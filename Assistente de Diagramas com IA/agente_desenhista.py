import os
from openai import AzureOpenAI
from dotenv import load_dotenv
import json
from mcp_client import get_library_docs # Importa o cliente MCP

# Carrega as variáveis de ambiente
load_dotenv()

# Configura o cliente da Azure OpenAI
client = AzureOpenAI(
    api_key=os.getenv("AZURE_OPENAI_KEY"),
    api_version=os.getenv("AZURE_OPENAI_API_VERSION"),
    azure_endpoint=os.getenv("AZURE_OPENAI_ENDPOINT")
)

deployment_name = os.getenv('AZURE_OPENAI_DEPLOYMENT_NAME')

def desenhar_diagrama_com_plano(plano: dict) -> tuple[str, str]:
    """
    Usa a IA para gerar o código Mermaid, combinando um plano de design e a documentação do MCP.

    Args:
        plano: Um dicionário contendo o plano de design estruturado.

    Returns:
        Uma tupla contendo o código Mermaid gerado e uma mensagem de log.
    """
    # 1. Consulta à documentação atualizada via MCP
    mermaid_docs = get_library_docs('/mermaid-js/mermaid', topic='flowchart syntax')
    plano_str = json.dumps(plano, indent=2)

    system_prompt = f"""
    Você é um especialista em desenhar diagramas com a sintaxe Mermaid. Sua tarefa é converter um "plano de design" JSON em um código Mermaid limpo e funcional.

    Você deve seguir DUAS fontes de conhecimento:
    1. O PLANO DE DESIGN: Ele define a estrutura, os passos, os textos e as conexões. Siga-o rigorosamente.
    2. A DOCUMENTAÇÃO DE REFERÊNCIA: Use-a para aplicar a sintaxe mais moderna e eficiente para os elementos definidos no plano.

    --- INÍCIO DA DOCUMENTAÇÃO DE REFERÊNCIA (MERMAID) ---
    {mermaid_docs}
    --- FIM DA DOCUMENTAÇÃO ---

    Analise o plano de design a seguir e gere APENAS o código Mermaid correspondente. Não inclua nenhuma explicação ou texto adicional.
    """

    try:
        response = client.chat.completions.create(
            model=deployment_name,
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": plano_str} # O plano JSON é o prompt do usuário
            ],
            temperature=0.0, # Temperatura zero para seguir o plano o mais fielmente possível
        )

        mermaid_code = response.choices[0].message.content

        # Limpa o código para retornar apenas o conteúdo dentro do bloco ```mermaid ... ```
        if '```mermaid' in mermaid_code:
            mermaid_code = mermaid_code.split('```mermaid')[1].split('```')[0].strip()
        elif '```' in mermaid_code:
             mermaid_code = mermaid_code.split('```')[1].strip()

        log_message = "✅ **Agente Desenhista**: Diagrama renderizado com sucesso, combinando o plano de design com a documentação do MCP."
        return mermaid_code, log_message

    except Exception as e:
        log_message = f"❌ **Agente Desenhista**: Falha ao desenhar o diagrama. Erro: {e}"
        return f"-- Erro ao desenhar diagrama: {e}", log_message
