# 📋 Estado Atual do Projeto - Assistente de Diagramas com IA

**Data da Documentação:** 2025-09-07 19:33:45  
**Versão:** 2.0 - ChromaDB Enhanced System  
**Status:** Totalmente Funcional e Aprimorado

---

## 🎯 Visão Geral do Sistema

Este projeto é um **Assistente de Diagramas com IA** que utiliza múltiplos agentes colaborativos para gerar diagramas Mermaid a partir de descrições em linguagem natural. O sistema foi completamente aprimorado com **ChromaDB** para busca semântica avançada e análise arquitetural automática.

### **Principais Funcionalidades:**
- ✅ **Geração Colaborativa de Diagramas** com 5 agentes especializados
- ✅ **Busca Semântica Inteligente** com ChromaDB
- ✅ **Orquestração Automática** de inicialização e sincronização
- ✅ **Explorador de Dados** completo com filtros e exportação
- ✅ **Visualização Interativa** do grafo de conhecimento
- ✅ **Interface Streamlit** com 4 abas organizadas

---

## 🏗️ Arquitetura do Sistema

### **Componentes Principais:**

#### **1. Agentes de IA (5 agentes especializados):**
- **`agente_analista.py`** - Analisa prompts e cria planos de design
- **`agente_critico.py`** - Avalia e fornece feedback sobre planos
- **`agente_desenhista.py`** - Converte planos em código Mermaid
- **`agente_validador.py`** - Valida sintaxe usando Mermaid CLI
- **`agente_corretor.py`** - Corrige erros de sintaxe identificados

#### **2. Orquestração e Gerenciamento:**
- **`app.py`** - Aplicação principal Streamlit (4 abas)
- **`api_orchestrator.py`** - Sistema de inicialização automática
- **`chroma_manager.py`** - Gerenciador completo do ChromaDB

#### **3. Base de Conhecimento:**
- **`knowledge_graph.json`** - Grafo de conhecimento com resumos detalhados
- **`project_dictionary.json`** - Dicionário completo dos componentes
- **`chroma_db/`** - Banco vetorial local para busca semântica

#### **4. Scripts Utilitários:**
- **`ingest_to_chroma.py`** - Script standalone de ingestão (deprecated)
- **`query_chroma.py`** - Interface tabular para ChromaDB
- **`visualize_knowledge_graph.py`** - Gerador de visualização HTML
- **`test_chroma_reingest.py`** - Script de teste do sistema aprimorado

---

## 📁 Estrutura de Diretórios

```
agente_diagrama/
├── Assistente de Diagramas com IA/
│   ├── __init__.py
│   ├── app.py                      # 🎯 Aplicação principal Streamlit
│   ├── api_orchestrator.py         # 🤖 Orquestração automática
│   ├── chroma_manager.py           # 🗄️ Gerenciador ChromaDB
│   ├── agente_analista.py          # 🧠 Agente Analista
│   ├── agente_critico.py           # 🔍 Agente Crítico
│   ├── agente_desenhista.py        # 🎨 Agente Desenhista
│   ├── agente_validador.py         # ✅ Agente Validador
│   ├── agente_corretor.py          # 🔧 Agente Corretor
│   ├── ingest_to_chroma.py         # 📥 Script ingestão (deprecated)
│   └── query_chroma.py             # 📊 Interface ChromaDB tabular
├── chroma_db/                      # 🗄️ Banco vetorial ChromaDB
├── diagrams/                       # 📈 Diagramas Mermaid gerados
├── frontend/
│   └── style.css                   # 🎨 Estilos da interface
├── agents/
│   └── analista_de_processos.md    # 📚 Documentação agentes
├── knowledge_graph.json            # 🕸️ Grafo de conhecimento
├── project_dictionary.json         # 📖 Dicionário do projeto
├── knowledge_graph.html            # 🌐 Visualização interativa
├── visualize_knowledge_graph.py    # 🎯 Gerador visualização
├── test_chroma_reingest.py         # 🧪 Teste sistema aprimorado
├── requirements.txt                # 📦 Dependências Python
├── .env                           # 🔐 Variáveis de ambiente
└── .gitignore                     # 🚫 Arquivos ignorados
```

---

## 🔧 Dependências e Configuração

### **Dependências Python (requirements.txt):**
```txt
streamlit>=1.28.0
streamlit-mermaid>=0.1.0
openai>=1.0.0
requests>=2.31.0
pyvis>=0.3.2
chromadb>=0.5.4
pandas>=2.0.0
```

### **Variáveis de Ambiente (.env):**
```env
# Azure OpenAI Configuration
AZURE_OPENAI_API_KEY=your_api_key_here
AZURE_OPENAI_ENDPOINT=https://your-resource.openai.azure.com/
AZURE_OPENAI_API_VERSION=2023-05-15
AZURE_OPENAI_DEPLOYMENT_NAME=your_deployment_name

# Optional: Mermaid CLI path (if not in PATH)
MERMAID_CLI_PATH=/path/to/mermaid/cli
```

### **Configuração ChromaDB:**
- **Tipo:** Banco vetorial local (sem necessidade de servidor)
- **Localização:** `./chroma_db/`
- **Coleção:** `knowledge_graph_collection`
- **Embedding:** Automático via ChromaDB

---

## 🚀 Como Executar

### **1. Instalação:**
```bash
# Clonar/copiar projeto para nova IDE
cd agente_diagrama

# Instalar dependências
pip install -r requirements.txt

# Configurar variáveis de ambiente
cp .env.example .env  # Editar com suas credenciais
```

### **2. Execução Principal:**
```bash
# Executar aplicação Streamlit
streamlit run "Assistente de Diagramas com IA/app.py"
```

### **3. Scripts Utilitários:**
```bash
# Testar sistema ChromaDB
python test_chroma_reingest.py

# Interface tabular ChromaDB
streamlit run "Assistente de Diagramas com IA/query_chroma.py"

# Gerar visualização do grafo
python visualize_knowledge_graph.py
```

---

## 🖥️ Interface do Usuário

### **Aba 1: Gerar Diagrama com IA**
- **Entrada:** Campo de texto para descrição do processo
- **Processo:** Orquestração automática dos 5 agentes
- **Saída:** Diagrama Mermaid renderizado + logs em tempo real
- **Funcionalidades:** Refinamento iterativo, validação automática

### **Aba 2: Explorar Grafo de Conhecimento**
- **Visualização:** Grafo interativo HTML com nós coloridos
- **Navegação:** Zoom, pan, seleção de nós
- **Informações:** Detalhes de componentes e relacionamentos

### **Aba 3: Busca Semântica no Grafo** ⭐ **APRIMORADA**
- **Busca:** Campo de consulta em linguagem natural
- **Sugestões:** Baseadas na análise semântica automática
- **Resultados:** Dashboard com estatísticas e filtros avançados
- **Filtros:** Por tipo, fonte, com resumos expandíveis
- **Exportação:** Individual e em lote (JSON)
- **Re-ingestão:** Botão para atualizar ChromaDB

### **Aba 4: Explorar ChromaDB** ⭐ **NOVA**
- **Dashboard:** Estatísticas gerais (total itens, tipos, relacionamentos)
- **Navegação:** Paginada com filtros por tipo e fonte
- **Visualização:** Metadados organizados e expandíveis
- **Estatísticas:** Por página com métricas em tempo real
- **Exportação:** Dados completos filtrados em JSON

---

## 🤖 Sistema de Orquestração Automática

### **Sequência de Inicialização:**
1. **📖 Leitura do Grafo** - Análise inicial da arquitetura
2. **🔄 Sincronização ChromaDB** - Verificação via hash SHA256
3. **🧠 Análise Semântica** - Profundidade semântica dos componentes
4. **📊 Geração de Insights** - Métricas e sugestões automáticas

### **Funcionalidades Automáticas:**
- **Detecção de Mudanças:** Hash SHA256 do knowledge_graph.json
- **Ingestão Inteligente:** Apenas quando necessário
- **Análise Semântica:** Identificação de novos componentes
- **Insights Contextuais:** Sugestões baseadas na arquitetura

---

## 🗄️ Sistema ChromaDB Aprimorado

### **Estrutura de Dados:**
```json
{
  "nodes": {
    "document": "ID: chroma_db, Tipo: database, Label: ChromaDB, Resumo: Base de dados vetorial...",
    "metadata": {
      "id": "chroma_db",
      "type": "database", 
      "label": "ChromaDB (Vector Store)",
      "summary": "Descrição detalhada...",
      "source": "node"
    }
  },
  "edges": {
    "document": "Edge from 'app.py' to 'chroma_manager.py' labeled 'uses'. Descrição: O orquestrador...",
    "metadata": {
      "source": "app.py",
      "target": "chroma_manager.py",
      "label": "uses",
      "description": "Descrição detalhada...",
      "source_type": "edge"
    }
  }
}
```

### **Funcionalidades ChromaDB:**
- **Ingestão Automática:** Nós e arestas com resumos/descrições
- **Busca Semântica:** Consultas em linguagem natural
- **Filtros Avançados:** Por tipo, fonte, metadados
- **Re-ingestão Forçada:** Atualização completa sob demanda
- **Exportação:** Dados estruturados em JSON

---

## 📊 Dados do Knowledge Graph

### **Tipos de Nós (19 componentes):**
- **`agent`** (5) - Agentes de IA especializados
- **`orchestrator`** (2) - app.py e api_orchestrator.py
- **`module`** (1) - chroma_manager.py
- **`database`** (1) - chroma_db
- **`ui_component`** (4) - Componentes de interface
- **`external_service`** (2) - OpenAI e Mermaid CLI
- **`knowledge_source`** (4) - Arquivos de documentação
- **`data_object`** (3) - Estruturas de dados
- **`script`** (2) - Scripts utilitários
- **`config`** (1) - requirements.txt

### **Relacionamentos (32 arestas):**
- **Orquestração:** app.py → agentes
- **Dados:** agentes → objetos de dados
- **Serviços:** agentes → OpenAI/Mermaid CLI
- **Gerenciamento:** chroma_manager → chroma_db
- **Interface:** app.py → componentes UI

---

## 🔍 Funcionalidades de Busca e Análise

### **Busca Semântica:**
- **Consultas Naturais:** "Como funciona o ChromaDB?"
- **Sugestões Inteligentes:** Baseadas na análise automática
- **Filtros Dinâmicos:** Por tipo de componente
- **Resultados Enriquecidos:** Com ícones, resumos e insights

### **Explorador de Dados:**
- **Navegação Paginada:** 10/25/50/100 itens por página
- **Filtros Múltiplos:** Tipo de dados, tipos de nós
- **Estatísticas Dinâmicas:** Por página e globais
- **Visualização Organizada:** Metadados categorizados

### **Exportação Avançada:**
- **Individual:** Por resultado de busca
- **Em Lote:** Dados filtrados completos
- **Formato JSON:** Estruturado com metadados
- **Configurável:** Filtros aplicados incluídos

---

## 🛠️ Manutenção e Desenvolvimento

### **Atualizações do Knowledge Graph:**
1. **Editar:** `knowledge_graph.json` (adicionar resumos/descrições)
2. **Executar:** `python visualize_knowledge_graph.py`
3. **Re-ingerir:** Usar botão na interface ou `chroma_manager.force_reingest()`

### **Adição de Novos Componentes:**
1. **Atualizar:** `knowledge_graph.json` com novo nó/aresta
2. **Documentar:** `project_dictionary.json` com detalhes
3. **Sincronizar:** ChromaDB detectará mudanças automaticamente

### **Debugging e Testes:**
- **Logs:** Visíveis na interface Streamlit
- **Teste ChromaDB:** `python test_chroma_reingest.py`
- **Interface Tabular:** `streamlit run query_chroma.py`
- **Validação:** Agente validador com Mermaid CLI

---

## 🚨 Problemas Conhecidos e Soluções

### **ChromaDB não sincroniza:**
```python
# Solução: Forçar re-ingestão
from chroma_manager import ChromaManager
cm = ChromaManager(".")
cm.force_reingest()
```

### **Agentes não respondem:**
- **Verificar:** Variáveis de ambiente Azure OpenAI
- **Testar:** Conectividade com endpoint
- **Logs:** Verificar mensagens de erro na interface

### **Mermaid CLI não encontrado:**
- **Instalar:** `npm install -g @mermaid-js/mermaid-cli`
- **Configurar:** Variável `MERMAID_CLI_PATH` no .env

### **Interface não carrega:**
- **Dependências:** `pip install -r requirements.txt`
- **Porta:** Streamlit usa porta 8501 por padrão
- **Firewall:** Verificar bloqueios locais

---

## 📈 Métricas e Performance

### **Capacidade Atual:**
- **Componentes:** 19 nós + 32 arestas = 51 elementos
- **ChromaDB:** ~38 documentos com embeddings
- **Busca:** Sub-segundo para consultas típicas
- **Interface:** Responsiva até 100 itens por página

### **Escalabilidade:**
- **ChromaDB:** Suporta milhões de documentos
- **Streamlit:** Paginação eficiente implementada
- **Agentes:** Paralelizáveis se necessário
- **Armazenamento:** Local, sem limites de rede

---

## 🎯 Próximos Passos Sugeridos

### **Melhorias Técnicas:**
1. **Cache Inteligente:** Para consultas frequentes
2. **Análise de Sentimentos:** Nos feedbacks dos agentes
3. **Métricas Avançadas:** Tempo de resposta, precisão
4. **API REST:** Para integração externa

### **Funcionalidades:**
1. **Histórico de Diagramas:** Versionamento e comparação
2. **Templates:** Diagramas pré-definidos
3. **Colaboração:** Multi-usuário em tempo real
4. **Integração:** Git, Confluence, Notion

### **Interface:**
1. **Temas:** Modo escuro/claro
2. **Personalização:** Layout configurável
3. **Mobile:** Responsividade aprimorada
4. **Acessibilidade:** Padrões WCAG

---

## 📞 Suporte e Contato

### **Documentação Técnica:**
- **Knowledge Graph:** `knowledge_graph.json`
- **Dicionário:** `project_dictionary.json`
- **Visualização:** `knowledge_graph.html`

### **Scripts de Diagnóstico:**
- **Teste Completo:** `python test_chroma_reingest.py`
- **Verificação ChromaDB:** Interface aba 4
- **Logs Detalhados:** Console Streamlit

### **Arquivos de Configuração:**
- **Ambiente:** `.env`
- **Dependências:** `requirements.txt`
- **Estilos:** `frontend/style.css`

---

**🎉 Sistema Totalmente Funcional e Documentado!**

Este documento fornece todas as informações necessárias para continuar o desenvolvimento em qualquer IDE. O sistema está em estado produtivo com todas as funcionalidades implementadas e testadas.
