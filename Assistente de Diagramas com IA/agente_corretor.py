from openai import AzureOpenAI
import os
from dotenv import load_dotenv
from mcp_client import get_library_docs # Importa o cliente MCP

# Define o caminho para o arquivo .env na pasta pai
dotenv_path = os.path.join(os.path.dirname(__file__), '..', '.env')

# Carrega as variáveis de ambiente do arquivo especificado
load_dotenv(dotenv_path=dotenv_path)

# Configurar o cliente Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT"),
)

deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")

def _ler_manual_de_boas_praticas():
    """Lê o conteúdo do manual de boas práticas."""
    try:
        manual_path = os.path.join(os.path.dirname(__file__), "manual_de_boas_praticas_mermaid.md")
        with open(manual_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Manual de boas práticas não encontrado."

def corrigir_diagrama_mermaid(codigo_invalido: str, mensagem_erro: str) -> tuple[str, str]:
    """
    Tenta corrigir um código Mermaid inválido usando a IA.

    Args:
        codigo_invalido: O código Mermaid com erro.
        mensagem_erro: A mensagem de erro retornada pelo validador.

    Returns:
        Uma tupla contendo o código Mermaid corrigido e uma mensagem de log detalhando a ação do agente.
    """
    # 1. Consulta ao conhecimento local (erros passados)
    manual_content = _ler_manual_de_boas_praticas()
    # 2. Consulta à documentação atualizada via MCP
    mermaid_docs = get_library_docs('/mermaid-js/mermaid', topic='flowchart syntax')

    prompt_sistema = f"""
    Você é um especialista em sintaxe de diagramas Mermaid. Sua tarefa é corrigir o código Mermaid fornecido.
    O código a seguir resultou no erro: '{mensagem_erro}'.

    Para garantir a sintaxe correta, você deve seguir DUAS fontes de conhecimento:
    1. O MANUAL DE BOAS PRÁTICAS, que contém lições de erros passados.
    2. A DOCUMENTAÇÃO DE REFERÊNCIA, que contém a sintaxe oficial mais recente.

    --- INÍCIO DO MANUAL DE BOAS PRÁTICAS ---
    {manual_content}
    --- FIM DO MANUAL DE BOAS PRÁTICAS ---

    --- INÍCIO DA DOCUMENTAÇÃO DE REFERÊNCIA (MERMAID) ---
    {mermaid_docs}
    --- FIM DA DOCUMENTAÇÃO ---

    Analise o código, o erro e as fontes de conhecimento para fornecer uma correção. Forneça apenas o código Mermaid corrigido, sem nenhuma explicação adicional.
    """

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": prompt_sistema},
                {"role": "user", "content": codigo_invalido}
            ],
            temperature=0.1, # Baixa temperatura para correções mais determinísticas
        )
        codigo_corrigido = response.choices[0].message.content
        # Limpa o código de possíveis blocos de markdown
        if codigo_corrigido.strip().startswith("```mermaid"):
            codigo_corrigido = codigo_corrigido.strip()[len("```mermaid"):].strip()
        if codigo_corrigido.strip().endswith("```"):
            codigo_corrigido = codigo_corrigido.strip()[:-len("```")].strip()
            
        log_message = "✅ **Agente Corretor**: Tentativa de correção aplicada com sucesso, usando o manual e a documentação do MCP."
        return codigo_corrigido, log_message

    except Exception as e:
        print(f"Ocorreu um erro ao chamar a API da OpenAI: {e}")
        log_message = f"❌ **Agente Corretor**: Falha ao tentar corrigir o diagrama. Erro: {e}"
        return f"Ocorreu um erro ao corrigir o diagrama: {e}", log_message
