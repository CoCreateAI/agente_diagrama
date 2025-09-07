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

def criticar_plano_de_design(prompt_original: str, plano_json_str: str) -> tuple[dict, str]:
    """
    Analisa um plano de design em relação ao prompt original e fornece críticas.

    Args:
        prompt_original: O texto descritivo inicial do usuário.
        plano_json_str: A string JSON do plano de design a ser criticado.

    Returns:
        Uma tupla contendo o resultado da crítica em JSON (como um dicionário) e uma mensagem de log.
    """
    system_prompt = f"""
    Você é um Auditor de Qualidade de Processos extremamente rigoroso. Sua tarefa é analisar um "Plano de Design" em JSON e compará-lo com o "Prompt Original" do usuário para garantir que o plano seja uma representação fiel, completa e lógica do processo descrito.

    Sua análise deve focar em três pontos principais:
    1.  **Completude**: O plano contempla TODAS as etapas, cenários e exceções descritas no prompt? (Ex: caminhos de sucesso, falha, recusa, etc.).
    2.  **Clareza**: Os nomes das etapas no plano são claros, específicos e fáceis de entender? Nomes genéricos como "Validar Dados" devem ser questionados se o prompt fornecer mais detalhes.
    3.  **Lógica**: A sequência das etapas e as conexões entre elas fazem sentido lógico de acordo com o processo descrito?

    Sua saída DEVE ser um objeto JSON com a seguinte estrutura:
    - Se o plano estiver perfeito, retorne: `{{"status": "Aprovado", "criticas": []}}`
    - Se o plano precisar de melhorias, retorne: `{{"status": "Requer Refinamento", "criticas": ["Crítica 1...", "Crítica 2..."]}}`

    Seja objetivo e direto. Gere APENAS o objeto JSON como resposta.
    """

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": f'--PROMPT ORIGINAL--\n{prompt_original}\n\n--PLANO DE DESIGN PARA ANÁLISE--\n{plano_json_str}'}
            ],
            temperature=0.0,
            response_format={"type": "json_object"}
        )

        critica_json_str = response.choices[0].message.content
        critica_dict = json.loads(critica_json_str)

        log_message = "✅ **Agente Crítico**: Análise de qualidade do plano concluída."
        return critica_dict, log_message

    except json.JSONDecodeError as e:
        log_message = f"❌ **Agente Crítico**: Falha ao decodificar o JSON da crítica. Erro: {e}"
        return {"status": "Erro", "criticas": [f"Falha na decodificação do JSON: {e}"]}, log_message
    except Exception as e:
        log_message = f"❌ **Agente Crítico**: Falha ao executar a crítica. Erro: {e}"
        return {"status": "Erro", "criticas": [f"Falha na chamada da IA: {e}"]}, log_message
