# ✅ Checklist de Migração para Nova IDE

## 📋 Pré-Migração

### Arquivos Essenciais para Copiar:
- [ ] **Pasta completa:** `agente_diagrama/`
- [ ] **Variáveis de ambiente:** `.env` (com suas credenciais)
- [ ] **Dependências:** `requirements.txt`
- [ ] **Base de conhecimento:** `knowledge_graph.json`
- [ ] **Dicionário:** `project_dictionary.json`
- [ ] **ChromaDB:** `chroma_db/` (pasta completa)

### Credenciais Necessárias:
- [ ] **Azure OpenAI API Key**
- [ ] **Azure OpenAI Endpoint**
- [ ] **Deployment Name**

## 🔧 Pós-Migração

### 1. Instalação:
```bash
cd agente_diagrama
pip install -r requirements.txt
```

### 2. Configuração:
- [ ] Criar/editar arquivo `.env`
- [ ] Verificar credenciais Azure OpenAI
- [ ] Testar conectividade

### 3. Verificação do Sistema:
```bash
# Teste ChromaDB
python test_chroma_reingest.py

# Teste aplicação
streamlit run "Assistente de Diagramas com IA/app.py"
```

### 4. Funcionalidades a Testar:
- [ ] **Aba 1:** Geração de diagrama funciona
- [ ] **Aba 2:** Visualização do grafo carrega
- [ ] **Aba 3:** Busca semântica retorna resultados
- [ ] **Aba 4:** Explorador ChromaDB mostra dados
- [ ] **Re-ingestão:** Botão funciona sem erros
- [ ] **Exportação:** Downloads funcionam

## 🚨 Troubleshooting

### ChromaDB não funciona:
```python
from chroma_manager import ChromaManager
cm = ChromaManager(".")
cm.force_reingest()
```

### Agentes não respondem:
- Verificar `.env`
- Testar endpoint Azure
- Verificar logs no Streamlit

### Interface não carrega:
- `pip install -r requirements.txt`
- Verificar porta 8501
- Reiniciar Streamlit

## 📊 Estado Atual Confirmado

✅ **19 componentes** no knowledge graph  
✅ **32 relacionamentos** mapeados  
✅ **4 abas** funcionais na interface  
✅ **ChromaDB** com busca semântica  
✅ **Orquestração automática** implementada  
✅ **Exportação completa** disponível  

## 📞 Suporte

- **Documentação completa:** `PROJETO_ESTADO_ATUAL.md`
- **Setup rápido:** `SETUP_RAPIDO.md`
- **Visualização:** `knowledge_graph.html`
