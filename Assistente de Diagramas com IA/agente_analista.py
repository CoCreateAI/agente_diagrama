import os
import json
from openai import AzureOpenAI
from dotenv import load_dotenv

# Define o caminho para o arquivo .env na pasta pai
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Carrega as variáveis de ambiente do arquivo especificado
load_dotenv(dotenv_path=dotenv_path)

# Configura o cliente da Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

def _ler_manual_de_design():
    """Lê o conteúdo do manual de boas práticas de design."""
    try:
        manual_path = os.path.join(os.path.dirname(__file__), "manual_de_boas_praticas_design.md")
        with open(manual_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Manual de design não encontrado."

def analisar_prompt_e_criar_plano(prompt_usuario: str, plano_anterior_str: str = None, criticas: list = None) -> tuple[dict, str]:
    """
    Analisa o prompt do usuário ou refina um plano existente com base em críticas.

    Args:
        prompt_usuario: O prompt original do usuário.
        plano_anterior_str: O plano JSON anterior (como string) a ser refinado.
        criticas: Uma lista de críticas a serem aplicadas.

    Returns:
        Uma tupla contendo o plano JSON (como dicionário) e uma mensagem de log.
    """
    manual_design = _ler_manual_de_design()
    is_refinement_cycle = plano_anterior_str and criticas

    if is_refinement_cycle:
        # Modo de Refinamento
        system_prompt = f"""
        Você é um especialista em Análise e Design de Processos. Sua tarefa é refinar um "Plano de Design" JSON com base em uma lista de "Críticas".
        O objetivo é garantir que o plano final seja uma representação fiel e completa do "Prompt Original" do usuário.
        
        Siga RIGOROSAMENTE as regras do manual de design para manter a consistência.
        --- INÍCIO DO MANUAL DE DESIGN ---
        {manual_design}
        --- FIM DO MANUAL ---

        Analise o plano anterior e as críticas, e gere uma nova versão do plano em JSON que resolva TODOS os pontos levantados. Gere APENAS o objeto JSON completo e atualizado.
        """
        criticas_str = "\n".join(f"- {c}" for c in criticas)
        user_content = f'--PROMPT ORIGINAL--\n{prompt_usuario}\n\n--PLANO ANTERIOR PARA REFINAR--\n{plano_anterior_str}\n\n--CRÍTICAS A SEREM APLICADAS--\n{criticas_str}'
        log_action = "refinado"
    else:
        # Modo de Criação Inicial
        system_prompt = f"""
        Você é um especialista em Análise e Design de Processos. Sua tarefa é converter a descrição de um processo, fornecida pelo usuário, em um plano de design estruturado em JSON.
        
        Siga RIGOROSAMENTE as regras e a estrutura de saída definidas no manual a seguir.
        --- INÍCIO DO MANUAL DE DESIGN ---
        {manual_design}
        --- FIM DO MANUAL ---

        Analise o prompt do usuário e gere APENAS o objeto JSON correspondente ao plano de design.
        """
        user_content = prompt_usuario
        log_action = "criado"

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_content}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        plano_json_str = response.choices[0].message.content
        plano_dict = json.loads(plano_json_str)

        log_message = f"✅ **Agente Analista**: Plano de design {log_action} com sucesso."
        return plano_dict, log_message

    except json.JSONDecodeError as e:
        log_message = f"❌ **Agente Analista**: Falha ao decodificar o JSON do plano. Erro: {e}"
        return {"erro": "Falha na decodificação do JSON", "detalhes": str(e)}, log_message
    except Exception as e:
        log_message = f"❌ **Agente Analista**: Falha ao criar o plano de design. Erro: {e}"
        return {"erro": "Falha na chamada da IA", "detalhes": str(e)}, log_message
