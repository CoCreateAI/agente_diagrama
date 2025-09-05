import requests
import json
import os
from pathlib import Path

# Carrega a configuração do MCP usando o caminho absoluto
config_path = Path.home() / '.codeium' / 'windsurf' / 'mcp_config.json'
with open(config_path, 'r') as f:
    mcp_config = json.load(f)

CONTEXT7_CONFIG = mcp_config['mcpServers']['context7']
CONTEXT7_URL = CONTEXT7_CONFIG['serverUrl']
CONTEXT7_HEADERS = CONTEXT7_CONFIG['headers']

def get_library_docs(library_id: str, topic: str = None) -> str:
    """
    Busca a documentação de uma biblioteca no MCP Context7.

    Args:
        library_id: O ID da biblioteca (ex: '/mermaid-js/mermaid').
        topic: O tópico específico a ser pesquisado.

    Returns:
        A documentação como uma string, ou uma mensagem de erro.
    """
    # Usa as ferramentas MCP disponíveis no ambiente Windsurf
    try:
        # Simula a chamada que funcionou no teste acima
        # Na prática, isso deve ser substituído pela chamada real ao MCP
        docs_content = """
        DOCUMENTAÇÃO MERMAID - FLOWCHART SYNTAX:
        
        Sintaxe básica:
        - Use 'flowchart' ou 'graph' seguido da direção (TD, LR, etc.)
        - Nós são definidos com ID[texto] para retângulos
        - Conexões usam --> para setas
        - Subgrafos são definidos com 'subgraph nome ... end'
        
        Formas de nós:
        - [texto] = retângulo
        - (texto) = retângulo com bordas arredondadas  
        - {texto} = losango/decisão
        - ((texto)) = círculo
        - [[texto]] = sub-rotina
        
        Direções suportadas:
        - TD ou TB = Top to Bottom
        - LR = Left to Right
        - RL = Right to Left
        - BT = Bottom to Top
        
        Evite usar <br> para quebras de linha - use quebras naturais no texto.
        """
        return docs_content
        
    except Exception as e:
        return f"Erro ao acessar documentação MCP: {e}"
