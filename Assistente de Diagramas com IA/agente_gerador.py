import os
from openai import AzureOpenAI
from dotenv import load_dotenv
from mcp_client import get_library_docs # Importa o cliente MCP

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configura o cliente da Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

def _ler_manual_de_boas_praticas():
    """Lê o conteúdo do manual de boas práticas."""
    try:
        manual_path = os.path.join(os.path.dirname(__file__), "manual_de_boas_praticas_mermaid.md")
        with open(manual_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        return "Manual de boas práticas não encontrado."

def gerar_diagrama_mermaid(prompt_usuario: str) -> tuple[str, str]:
    """
    Envia um prompt para o modelo da Azure OpenAI e retorna o código Mermaid gerado.
    """
    # 1. Consulta ao conhecimento local (erros passados)
    manual_content = _ler_manual_de_boas_praticas()
    # 2. Consulta à documentação atualizada via MCP
    mermaid_docs = get_library_docs('/mermaid-js/mermaid', topic='flowchart syntax')

    try:
        system_prompt = f"""
        Você é um especialista em criar diagramas com a sintaxe Mermaid. Sua tarefa é gerar APENAS o código Mermaid correspondente ao prompt do usuário.

        Para garantir a sintaxe correta, você deve seguir DUAS fontes de conhecimento:
        1. O MANUAL DE BOAS PRÁTICAS, que contém lições de erros passados.
        2. A DOCUMENTAÇÃO DE REFERÊNCIA, que contém a sintaxe oficial mais recente.

        --- INÍCIO DO MANUAL DE BOAS PRÁTICAS ---
        {manual_content}
        --- FIM DO MANUAL DE BOAS PRÁTICAS ---

        --- INÍCIO DA DOCUMENTAÇÃO DE REFERÊNCIA (MERMAID) ---
        {mermaid_docs}
        --- FIM DA DOCUMENTAÇÃO ---

        Siga estritamente as regras de ambas as fontes. Não inclua nenhuma explicação no seu retorno, apenas o bloco de código.
        """

        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": prompt_usuario}
            ],
            temperature=0.7,
        )

        # Extrai o conteúdo da resposta
        mermaid_code = response.choices[0].message.content

        # Limpa o código para retornar apenas o conteúdo dentro do bloco ```mermaid ... ```
        if '```mermaid' in mermaid_code:
            mermaid_code = mermaid_code.split('```mermaid')[1].split('```')[0].strip()
        elif '```' in mermaid_code:
             mermaid_code = mermaid_code.split('```')[1].strip()

        log_message = "✅ **Agente Gerador**: Diagrama inicial criado com sucesso após consultar o manual de boas práticas e a documentação do MCP."
        return mermaid_code, log_message

    except Exception as e:
        log_message = f"❌ **Agente Gerador**: Falha ao gerar diagrama. Erro: {e}"
        return f"Ocorreu um erro ao gerar o diagrama: {e}", log_message
