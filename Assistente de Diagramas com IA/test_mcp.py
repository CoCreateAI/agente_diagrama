#!/usr/bin/env python3
"""
Script de teste para verificar a conectividade com o MCP Context7
"""
import requests
import json
from pathlib import Path

def test_mcp_connection():
    """Testa a conexão com o servidor MCP Context7"""
    
    # Carrega a configuração
    try:
        config_path = Path.home() / '.codeium' / 'windsurf' / 'mcp_config.json'
        print(f"Carregando configuração de: {config_path}")
        
        with open(config_path, 'r') as f:
            mcp_config = json.load(f)
        
        context7_config = mcp_config['mcpServers']['context7']
        url = context7_config['serverUrl']
        headers = context7_config['headers']
        
        print(f"URL do servidor: {url}")
        print(f"Headers: {headers}")
        
    except Exception as e:
        print(f"Erro ao carregar configuração: {e}")
        return False
    
    # Testa a conexão básica
    print("\n--- Testando conexão básica ---")
    try:
        response = requests.get(url, headers=headers, timeout=10)
        print(f"Status da resposta: {response.status_code}")
        print(f"Headers da resposta: {dict(response.headers)}")
        
    except Exception as e:
        print(f"Erro na conexão básica: {e}")
    
    # Testa uma chamada MCP específica
    print("\n--- Testando chamada MCP ---")
    payload = {
        'jsonrpc': '2.0',
        'method': 'get-library-docs',
        'params': {
            'context7CompatibleLibraryID': '/mermaid-js/mermaid',
            'topic': 'flowchart syntax'
        },
        'id': 1
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload, timeout=30)
        print(f"Status da resposta: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            print(f"Resposta JSON: {json.dumps(result, indent=2)[:500]}...")
            
            if 'result' in result:
                print("✅ Sucesso! MCP retornou dados.")
                return True
            elif 'error' in result:
                print(f"❌ Erro do MCP: {result['error']}")
            else:
                print("❌ Resposta inesperada do MCP")
        else:
            print(f"❌ Erro HTTP: {response.status_code}")
            print(f"Resposta: {response.text}")
            
    except Exception as e:
        print(f"❌ Erro na chamada MCP: {e}")
    
    return False

if __name__ == "__main__":
    print("=== Teste de Conectividade MCP Context7 ===")
    success = test_mcp_connection()
    
    if success:
        print("\n✅ MCP está funcionando corretamente!")
    else:
        print("\n❌ MCP não está funcionando. Verifique a configuração.")
