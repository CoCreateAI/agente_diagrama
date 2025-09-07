import streamlit as st
from streamlit_mermaid import st_mermaid
import os
import json
import streamlit.components.v1 as components
from agente_analista import analisar_prompt_e_criar_plano
from agente_desenhista import desenhar_diagrama_com_plano
from agente_validador import validar_diagrama_mermaid
from agente_corretor import corrigir_diagrama_mermaid
from agente_critico import criticar_plano_de_design
from chroma_manager import ChromaManager

# --- Configuração da Página ---
st.set_page_config(
    page_title="CoCreateAI | Assistente de Diagramas", 
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- Estilo Customizado (CSS) ---
with open(os.path.join(os.path.dirname(__file__), "..", "frontend", "style.css"), encoding="utf-8") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

# --- Título e Cabeçalho ---
st.title("Assistente de Diagramas com IA")
st.markdown("Descreva um processo, e os agentes de IA irão colaborar para criar um diagrama Mermaid para você.")

# --- Inicialização Automática com API Orchestrator ---
base_dir = os.path.dirname(os.path.dirname(__file__))

# Importar o orquestrador após definir base_dir
from api_orchestrator import APIOrchestrator

# Inicializar o sistema automaticamente
if 'orchestrator' not in st.session_state:
    st.session_state.orchestrator = APIOrchestrator(base_dir)
    
if 'system_initialized' not in st.session_state:
    with st.spinner('🤖 Inicializando sistema automático: lendo grafo → sincronizando ChromaDB → análise semântica...'):
        import asyncio
        
        # Executar inicialização automática
        loop = asyncio.new_event_loop()
        asyncio.set_event_loop(loop)
        initialization_report = loop.run_until_complete(st.session_state.orchestrator.initialize_system())
        loop.close()
        
        st.session_state.initialization_report = initialization_report
        st.session_state.system_initialized = True
        
        if initialization_report["status"] == "completed":
            st.success("✅ Sistema inicializado com análise semântica completa!")
            
            # Mostrar resumo da arquitetura
            arch_summary = st.session_state.orchestrator.get_architecture_summary()
            st.info(f"📊 **Resumo da Arquitetura**: {arch_summary['total_components']} componentes, "
                   f"profundidade semântica: {arch_summary['semantic_depth']:.2f}, "
                   f"{arch_summary['new_components']} novos componentes detectados")
        else:
            st.error("❌ Erro na inicialização do sistema")
            if initialization_report.get("errors"):
                for error in initialization_report["errors"]:
                    st.error(f"Erro: {error}")

# Manter referência ao chroma_manager para compatibilidade
chroma_manager = st.session_state.orchestrator.chroma_manager

# --- Estado da Sessão ---
if 'mermaid_code' not in st.session_state:
    st.session_state.mermaid_code = """graph TD
    subgraph "Fluxo de Ingestão e Construção da Base"
        A1["Fontes de Dados
(Texto, Arquivos, APIs)"] --> A2(Coletor)
        A2 --> A3(Normalizador & Carimbador)
        A3 --> A4(Curador de Memória)
        A4 --> A5(Anotador/Extrator)
        A5 --> A6(Ligador de Grafo)
        A6 --> A7(Indexador)
        A7 --> A8((Memória Pronta))
    end

    subgraph "Armazenamento de Conhecimento"
        S1["Grafo
(Entidades, Relações)"]
        S2["Banco NoSQL
(Documentos, Chunks)"]
        S3["Índice Vetorial/Lexical"]
        S4["Log de Eventos"]
    end

    subgraph "Fluxo de Consulta e Resposta"
        B1[Usuário] --> B2{Orquestrador de Consulta}
        B2 --> B3["Plano de
Recuperação"]
        B3 --> B4(Reranker & Seletor)
        B4 --> B2
        B2 --> B5[LLM]
        B5 --> B6(Crítico/Verificador)
        B6 -- Resposta Válida --> B7[Resposta ao Usuário]
        B6 -- Falha na Validação --> B2
    end

    subgraph "Fluxo de Evolução e Qualidade"
        C1["Feedback do Usuário
(explícito/implícito)"] --> C2(Coletor de Feedback)
        C2 --> C3(Avaliador Offline/Online)
        C3 --> C4(Otimizador de Políticas)
        C4 --> C5((Políticas Atualizadas))
    end

    %% Conexões entre os Fluxos
    A8 --> S1
    A8 --> S2
    A8 --> S3
    A8 --> S4

    B3 --> S1
    B3 --> S2
    B3 --> S3

    B7 --> C1

    C5 --> B2
    C5 --> B4
    C5 --> B6
    C5 --> A8

    classDef data fill:#e6f3ff,stroke:#007bff,stroke-width:2px
    classDef agent fill:#e0f7fa,stroke:#00796b,stroke-width:2px
    classDef system fill:#fff9c4,stroke:#fbc02d,stroke-width:2px
    classDef feedback fill:#f3e5f5,stroke:#8e24aa,stroke-width:2px

    class A1,S1,S2,S3,S4,A8,C5 data
    class A2,A3,A4,A5,A6,A7,B2,B4,B5,B6,C2,C3,C4 agent
    class B1,B7,C1 feedback
"""

# --- Layout Principal com Abas ---
tab1, tab2, tab3, tab4 = st.tabs(["Gerar Diagrama com IA", "Explorar Grafo de Conhecimento", "Busca Semântica no Grafo", "Explorar ChromaDB"])

with tab1:
    st.header("Crie um Diagrama com Inteligência Artificial")

    # Inicializa a lista de logs na sessão se não existir
    if 'log_messages' not in st.session_state:
        st.session_state.log_messages = []

    # Dividir a tela em duas colunas
    col1, col2 = st.columns([2, 1])

    with col1:
        prompt_usuario = st.text_area("Descreva o diagrama que você quer criar:", height=250, placeholder="Ex: Crie um fluxograma de um processo de login com sucesso e falha.")
        
        if st.button("Gerar Diagrama"):
            st.session_state.log_messages.clear()
            
            if prompt_usuario:
                max_tentativas = 3
                codigo_atual = ""
                mensagem_erro = ""

                with st.spinner("Os agentes estão trabalhando..."):
                    st.session_state.log_messages.append("▶️ **Iniciando processo**: Prompt do usuário recebido.")
                    
                    # --- Ciclo de Análise, Crítica e Refinamento do Plano ---
                    plano_atual = None
                    plano_aprovado = False
                    max_ciclos_refinamento = 3

                    # Etapa 1: Geração do plano inicial
                    plano_atual, log_analista = analisar_prompt_e_criar_plano(prompt_usuario)
                    st.session_state.log_messages.append(log_analista)

                    if "erro" in plano_atual:
                        st.error("O Agente Analista falhou em criar o plano inicial.")
                        st.session_state.log_messages.append("❌ **Processo finalizado com falha crítica na análise.**")
                        st.stop()

                    for ciclo in range(max_ciclos_refinamento):
                        st.session_state.log_messages.append(f"▶️ **Ciclo de Qualidade {ciclo + 1}/{max_ciclos_refinamento}**: Acionando Agente Crítico.")
                        
                        # Etapa 2: Agente Crítico analisa o plano
                        plano_atual_str = json.dumps(plano_atual, indent=2)
                        critica, log_critico = criticar_plano_de_design(prompt_usuario, plano_atual_str)
                        st.session_state.log_messages.append(log_critico)

                        if critica.get("status") == "Aprovado":
                            st.session_state.log_messages.append("✅ **Agente Crítico**: Plano de design aprovado.")
                            plano_aprovado = True
                            break
                        elif critica.get("status") == "Requer Refinamento":
                            criticas_list = critica.get('criticas', [])
                            st.session_state.log_messages.append(f"⚠️ **Agente Crítico**: Plano requer refinamento. Críticas: {', '.join(criticas_list)}")
                            
                            # Etapa 3: Agente Analista refina o plano
                            plano_atual, log_analista_refino = analisar_prompt_e_criar_plano(
                                prompt_usuario=prompt_usuario,
                                plano_anterior_str=plano_atual_str,
                                criticas=criticas_list
                            )
                            st.session_state.log_messages.append(log_analista_refino)
                            if "erro" in plano_atual:
                                st.error("O Agente Analista falhou durante o ciclo de refinamento.")
                                st.session_state.log_messages.append("❌ **Processo finalizado com falha crítica no refinamento.**")
                                plano_aprovado = False
                                break
                        else:
                            st.error("O Agente Crítico encontrou um erro inesperado.")
                            st.session_state.log_messages.append(f"❌ **Processo finalizado com falha crítica na auditoria.** Detalhes: {critica.get('criticas', ['N/A'])}")
                            plano_aprovado = False
                            break
                    
                    if not plano_aprovado:
                        st.session_state.log_messages.append("⚠️ **Aviso**: O plano não foi formalmente aprovado. Prosseguindo com a melhor versão disponível após os ciclos de refinamento.")
                    
                    # --- Ciclo de Desenho e Validação de Sintaxe ---
                    log_desenho = "com plano aprovado" if plano_aprovado else "com a melhor versão do plano"
                    st.session_state.log_messages.append(f"▶️ **Iniciando fase de desenho** {log_desenho}.")
                    
                    # Etapa 4: Agente Desenhista cria o código
                    codigo_atual, log_desenhista = desenhar_diagrama_com_plano(plano_atual)
                    st.session_state.log_messages.append(log_desenhista)

                    # Etapa 5: Validação e Correção de Sintaxe
                    max_tentativas_sintaxe = 3
                    for tentativa in range(max_tentativas_sintaxe):
                        valido, mensagem_erro, log_validador = validar_diagrama_mermaid(codigo_atual)
                        st.session_state.log_messages.append(log_validador)

                        if valido:
                            st.session_state.mermaid_code = codigo_atual
                            st.session_state.log_messages.append("✅ **Processo finalizado com sucesso.**")
                            break
                        else:
                            st.session_state.log_messages.append(f"▶️ **Iniciando correção de sintaxe {tentativa + 1}/{max_tentativas_sintaxe}**...")
                            codigo_atual, log_corretor = corrigir_diagrama_mermaid(codigo_atual, mensagem_erro)
                            st.session_state.log_messages.append(log_corretor)
                    else: 
                        st.error("Não foi possível gerar um diagrama com sintaxe válida após várias tentativas.")
                        st.session_state.log_messages.append("❌ **Processo finalizado com falha na correção de sintaxe.**")
                        st.session_state.mermaid_code = codigo_atual
            else:
                st.warning("Por favor, insira uma descrição para o diagrama.")
            
            # Força o rerender para exibir os logs imediatamente
            st.rerun()

        st.subheader("Diagrama Gerado")
        st_mermaid(st.session_state.mermaid_code, height="800px")

    with col2:
        st.subheader("Diálogo dos Agentes")
        if st.session_state.log_messages:
            log_container = st.container(border=True)
            for msg in st.session_state.log_messages:
                log_container.info(msg)

with tab2:
    st.header("Visualizador do Grafo de Conhecimento")
    html_path = os.path.join(base_dir, 'knowledge_graph.html')
    if os.path.exists(html_path):
        with open(html_path, 'r', encoding='utf-8') as f:
            source_code = f.read()
            components.html(source_code, height=800, scrolling=True)
    else:
        st.error("Arquivo 'knowledge_graph.html' não encontrado.")

with tab3:
    st.header("Busca Semântica Inteligente no Grafo de Conhecimento")
    
    # Mostrar insights da inicialização automática
    if hasattr(st.session_state, 'initialization_report'):
        report = st.session_state.initialization_report
        if report["status"] == "completed":
            with st.expander("📈 Relatório de Análise Automática", expanded=False):
                for step in report["steps"]:
                    if step["status"] == "completed":
                        st.success(f"✅ {step['step']}: {step.get('details', {})}")
                    else:
                        st.error(f"❌ {step['step']}: {step.get('error', 'Erro desconhecido')}")
    
    # Interface de busca aprimorada
    col1, col2 = st.columns([2, 1])
    
    with col1:
        query_text = st.text_input("Faça uma pergunta sobre a arquitetura:", 
                                 placeholder="Ex: Como funciona a integração com ChromaDB?")
        
        # Sugestões baseadas nos insights semânticos
        if hasattr(st.session_state, 'orchestrator'):
            st.write("💡 **Sugestões baseadas na análise semântica:**")
            suggestions = [
                "Quais são os componentes novos da arquitetura?",
                "Como funciona o fluxo de dados entre os agentes?",
                "Qual a profundidade semântica do sistema?",
                "Quais nós têm maior conectividade?"
            ]
            
            selected_suggestion = st.selectbox("Ou escolha uma sugestão:", 
                                             [""] + suggestions, 
                                             key="suggestion_select")
            if selected_suggestion:
                query_text = selected_suggestion
    
    with col2:
        st.write("🎯 **Análise Semântica Ativa**")
        if hasattr(st.session_state, 'orchestrator'):
            arch_summary = st.session_state.orchestrator.get_architecture_summary()
            st.metric("Componentes", arch_summary['total_components'])
            st.metric("Profundidade Semântica", f"{arch_summary['semantic_depth']:.2f}")
            st.metric("Novos Componentes", arch_summary['new_components'])
            
            # Botão para forçar re-ingestão
            if st.button("🔄 Forçar Re-ingestão", help="Atualiza completamente o ChromaDB com os dados mais recentes"):
                with st.spinner("Executando re-ingestão completa..."):
                    try:
                        chroma_manager.force_reingest()
                        st.success("✅ Re-ingestão concluída com sucesso!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"❌ Erro na re-ingestão: {e}")
    
    if st.button("🔍 Buscar com Análise Profunda", key="semantic_search"):
        if query_text:
            with st.spinner("Executando busca semântica inteligente..."):
                # Busca tradicional
                results = chroma_manager.semantic_query(query_text, n_results=5)
                
                st.subheader("📋 Resultados da Busca Semântica:")
                
                if results and results['documents'] and results['documents'][0]:
                    # Dashboard de estatísticas dos resultados
                    with st.container():
                        st.subheader("📊 Dashboard dos Resultados")
                        
                        # Análise dos tipos encontrados
                        types_found = {}
                        for metadata in results['metadatas'][0]:
                            node_type = metadata.get('type', 'Unknown')
                            types_found[node_type] = types_found.get(node_type, 0) + 1
                        
                        cols = st.columns(len(types_found) if types_found else 1)
                        for i, (type_name, count) in enumerate(types_found.items()):
                            with cols[i % len(cols)]:
                                st.metric(f"Tipo: {type_name}", count)
                    
                    st.divider()
                    
                    # Filtros avançados
                    with st.expander("🔧 Filtros Avançados", expanded=False):
                        filter_col1, filter_col2 = st.columns(2)
                        
                        with filter_col1:
                            selected_types = st.multiselect(
                                "Filtrar por Tipo:",
                                options=list(types_found.keys()),
                                default=list(types_found.keys())
                            )
                        
                        with filter_col2:
                            show_summaries = st.checkbox("Mostrar Resumos Completos", value=True)
                            include_edges = st.checkbox("Incluir Relacionamentos", value=False)
                    
                    # Mostrar resultados filtrados em formato aprimorado
                    filtered_results = []
                    for i, doc in enumerate(results['documents'][0]):
                        metadata = results['metadatas'][0][i]
                        if metadata.get('type', 'Unknown') in selected_types:
                            filtered_results.append((i, doc, metadata))
                    
                    st.write(f"**{len(filtered_results)} resultados encontrados:**")
                    
                    for result_idx, (i, doc, metadata) in enumerate(filtered_results):
                        with st.container():
                            # Cabeçalho do resultado com ícone baseado no tipo
                            type_icons = {
                                'agent': '🤖',
                                'database': '🗄️',
                                'module': '📦',
                                'orchestrator': '🎯',
                                'ui_component': '🖥️',
                                'external_service': '🌐',
                                'knowledge_source': '📚',
                                'data_object': '📄',
                                'script': '📜',
                                'config': '⚙️'
                            }
                            
                            icon = type_icons.get(metadata.get('type', ''), '📋')
                            st.markdown(f"### {icon} **Resultado {result_idx+1}: {metadata.get('label', 'N/A')}**")
                            
                            # Documento principal
                            st.info(doc)
                            
                            # Metadados organizados
                            meta_cols = st.columns(4)
                            with meta_cols[0]:
                                st.caption(f"**🏷️ Tipo:** {metadata.get('type', 'N/A')}")
                            with meta_cols[1]:
                                st.caption(f"**🆔 ID:** {metadata.get('id', 'N/A')}")
                            with meta_cols[2]:
                                st.caption(f"**📍 Fonte:** {metadata.get('source', 'N/A')}")
                            with meta_cols[3]:
                                if 'label' in metadata:
                                    st.caption(f"**📝 Label:** {metadata['label']}")
                            
                            # Resumo expandido se disponível
                            if show_summaries and 'summary' in metadata and metadata['summary']:
                                with st.expander("📖 Resumo Detalhado", expanded=False):
                                    st.markdown(metadata['summary'])
                            
                            # Insights semânticos específicos do nó
                            if hasattr(st.session_state, 'orchestrator'):
                                node_insights = st.session_state.orchestrator.get_semantic_insights_for_node(metadata.get('id'))
                                if node_insights:
                                    with st.expander("🧠 Insights Semânticos", expanded=False):
                                        st.json(node_insights)
                            
                            # Botão de exportação individual
                            export_data = {
                                'document': doc,
                                'metadata': metadata,
                                'semantic_insights': node_insights if hasattr(st.session_state, 'orchestrator') else None
                            }
                            
                            if st.button(f"📤 Exportar Resultado {result_idx+1}", key=f"export_{i}"):
                                st.download_button(
                                    label="💾 Download JSON",
                                    data=str(export_data),
                                    file_name=f"resultado_{metadata.get('id', 'unknown')}.json",
                                    mime="application/json",
                                    key=f"download_{i}"
                                )
                            
                            st.divider()
                else:
                    st.warning("Nenhum resultado encontrado.")
                    
                    # Sugerir consultas alternativas
                    st.info("💡 Tente consultas como: 'agentes', 'ChromaDB', 'interface', 'dados'")
        else:
            st.warning("Por favor, insira uma pergunta ou selecione uma sugestão.")

with tab4:
    st.header("🗄️ Explorador de Dados ChromaDB")
    
    # Estatísticas gerais do ChromaDB
    try:
        all_data = chroma_manager.get_all_data()
        total_items = all_data['total_items']
        
        # Dashboard principal
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("📊 Total de Itens", total_items)
        
        with col2:
            # Contar tipos de nós
            node_types = {}
            for metadata in all_data.get('metadatas', []):
                if metadata.get('source') == 'node':
                    node_type = metadata.get('type', 'Unknown')
                    node_types[node_type] = node_types.get(node_type, 0) + 1
            st.metric("🏷️ Tipos de Nós", len(node_types))
        
        with col3:
            # Contar relacionamentos
            edge_count = sum(1 for metadata in all_data.get('metadatas', []) 
                           if metadata.get('source_type') == 'edge')
            st.metric("🔗 Relacionamentos", edge_count)
        
        st.divider()
        
        # Navegador de dados
        st.subheader("🔍 Navegador de Dados")
        
        # Filtros
        filter_col1, filter_col2, filter_col3 = st.columns(3)
        
        with filter_col1:
            data_type_filter = st.selectbox(
                "Tipo de Dados:",
                ["Todos", "Apenas Nós", "Apenas Relacionamentos"]
            )
        
        with filter_col2:
            if node_types:
                selected_node_types = st.multiselect(
                    "Tipos de Nós:",
                    options=list(node_types.keys()),
                    default=list(node_types.keys())
                )
            else:
                selected_node_types = []
        
        with filter_col3:
            items_per_page = st.selectbox("Itens por página:", [10, 25, 50, 100], index=1)
        
        # Filtrar dados
        filtered_data = []
        for i, metadata in enumerate(all_data.get('metadatas', [])):
            document = all_data.get('documents', [None])[i] if i < len(all_data.get('documents', [])) else None
            
            # Aplicar filtros
            if data_type_filter == "Apenas Nós" and metadata.get('source') != 'node':
                continue
            elif data_type_filter == "Apenas Relacionamentos" and metadata.get('source_type') != 'edge':
                continue
            
            if metadata.get('source') == 'node' and metadata.get('type') not in selected_node_types:
                continue
                
            filtered_data.append((document, metadata))
        
        # Paginação
        total_filtered = len(filtered_data)
        total_pages = (total_filtered - 1) // items_per_page + 1 if total_filtered > 0 else 1
        
        page_col1, page_col2, page_col3 = st.columns([1, 2, 1])
        with page_col2:
            current_page = st.number_input(
                f"Página (1-{total_pages}):",
                min_value=1,
                max_value=total_pages,
                value=1
            )
        
        # Mostrar dados da página atual
        start_idx = (current_page - 1) * items_per_page
        end_idx = min(start_idx + items_per_page, total_filtered)
        page_data = filtered_data[start_idx:end_idx]
        
        st.write(f"**Mostrando {len(page_data)} de {total_filtered} itens:**")
        
        # Exibir dados em formato de tabela expandível
        for idx, (document, metadata) in enumerate(page_data):
            with st.expander(f"📋 Item {start_idx + idx + 1}: {metadata.get('label', metadata.get('id', 'N/A'))}", expanded=False):
                
                # Informações básicas
                info_cols = st.columns(2)
                
                with info_cols[0]:
                    st.write("**📄 Documento:**")
                    st.code(document or "N/A", language="text")
                
                with info_cols[1]:
                    st.write("**🏷️ Metadados:**")
                    
                    # Organizar metadados por categoria
                    basic_info = {}
                    extended_info = {}
                    
                    for key, value in metadata.items():
                        if key in ['id', 'type', 'label', 'source', 'source_type']:
                            basic_info[key] = value
                        else:
                            extended_info[key] = value
                    
                    # Mostrar informações básicas
                    for key, value in basic_info.items():
                        st.write(f"**{key.title()}:** {value}")
                    
                    # Mostrar informações estendidas se existirem
                    if extended_info:
                        with st.expander("Informações Detalhadas", expanded=False):
                            for key, value in extended_info.items():
                                if key == 'summary' and value:
                                    st.write(f"**📖 {key.title()}:**")
                                    st.markdown(value)
                                elif key == 'description' and value:
                                    st.write(f"**📝 {key.title()}:**")
                                    st.markdown(value)
                                else:
                                    st.write(f"**{key.title()}:** {value}")
        
        # Estatísticas da página atual
        if page_data:
            st.divider()
            st.subheader("📈 Estatísticas da Página Atual")
            
            page_stats_cols = st.columns(4)
            
            # Contar tipos na página atual
            page_types = {}
            page_sources = {}
            
            for _, metadata in page_data:
                # Tipos
                item_type = metadata.get('type', 'Unknown')
                page_types[item_type] = page_types.get(item_type, 0) + 1
                
                # Fontes
                source = metadata.get('source', metadata.get('source_type', 'Unknown'))
                page_sources[source] = page_sources.get(source, 0) + 1
            
            with page_stats_cols[0]:
                st.metric("Itens na Página", len(page_data))
            
            with page_stats_cols[1]:
                st.metric("Tipos Únicos", len(page_types))
            
            with page_stats_cols[2]:
                most_common_type = max(page_types.items(), key=lambda x: x[1]) if page_types else ("N/A", 0)
                st.metric("Tipo Mais Comum", f"{most_common_type[0]} ({most_common_type[1]})")
            
            with page_stats_cols[3]:
                st.metric("Fontes Únicas", len(page_sources))
        
        # Botão de exportação completa
        st.divider()
        if st.button("📤 Exportar Todos os Dados Filtrados"):
            import json
            export_data = {
                'total_items': total_filtered,
                'filters_applied': {
                    'data_type': data_type_filter,
                    'selected_node_types': selected_node_types
                },
                'data': [{'document': doc, 'metadata': meta} for doc, meta in filtered_data]
            }
            
            st.download_button(
                label="💾 Download Dados Completos (JSON)",
                data=json.dumps(export_data, indent=2, ensure_ascii=False),
                file_name=f"chromadb_export_{len(filtered_data)}_items.json",
                mime="application/json"
            )
    
    except Exception as e:
        st.error(f"❌ Erro ao acessar dados do ChromaDB: {e}")
        st.info("💡 Tente executar uma re-ingestão na aba de Busca Semântica.")
