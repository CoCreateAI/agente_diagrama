# 🚀 Setup Rápido - Assistente de Diagramas com IA

## ⚡ Início Imediato

### 1. **Dependências:**
```bash
pip install -r requirements.txt
```

### 2. **Configuração (.env):**
```env
AZURE_OPENAI_API_KEY=sua_chave_aqui
AZURE_OPENAI_ENDPOINT=https://seu-recurso.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=seu_deployment
```

### 3. **Executar:**
```bash
streamlit run "Assistente de Diagramas com IA/app.py"
```

## 🎯 Interface (4 Abas)

1. **Gerar Diagrama** - Criar diagramas com IA
2. **Explorar Grafo** - Visualização interativa
3. **Busca Semântica** - ChromaDB com filtros avançados
4. **Explorar ChromaDB** - Navegador completo de dados

## 🔧 Scripts Úteis

- **Teste ChromaDB:** `python test_chroma_reingest.py`
- **Visualizar Grafo:** `python visualize_knowledge_graph.py`
- **Interface Tabular:** `streamlit run "Assistente de Diagramas com IA/query_chroma.py"`

## 📁 Arquivos Principais

- **`app.py`** - Aplicação principal
- **`knowledge_graph.json`** - Base de conhecimento
- **`chroma_manager.py`** - Gerenciador ChromaDB
- **`api_orchestrator.py`** - Orquestração automática

## ✅ Status: Sistema Completo e Funcional
