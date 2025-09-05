import streamlit as st
from streamlit_mermaid import st_mermaid
import os
import json
from agente_analista import analisar_prompt_e_criar_plano
from agente_desenhista import desenhar_diagrama_com_plano
from agente_validador import validar_diagrama_mermaid
from agente_corretor import corrigir_diagrama_mermaid
from agente_critico import criticar_plano_de_design

# --- Configuração da Página ---
st.set_page_config(page_title="Mermaid AI Assistant", layout="wide")
st.title("Assistente de Diagramas com IA")

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

# --- Barra Lateral ---
st.sidebar.header("Modo de Operação")
app_mode = st.sidebar.radio("Escolha o que deseja fazer:", ('Visualizar Arquivos', 'Gerar com IA'))

# --- Modo: Visualizar Arquivos ---
if app_mode == 'Visualizar Arquivos':
    st.header("Visualizador de Diagramas Locais")
    # Constrói o caminho para a pasta de diagramas, que está um nível acima
    diagrams_dir = os.path.join(os.path.dirname(__file__), "..", "diagrams")

    if not os.path.isdir(diagrams_dir):
        st.error(f"A pasta '{diagrams_dir}' não foi encontrada.")
    else:
        diagram_files = [f for f in os.listdir(diagrams_dir) if f.endswith(".mmd")]
        if not diagram_files:
            st.warning(f"Nenhum arquivo .mmd encontrado na pasta '{diagrams_dir}'.")
        else:
            st.sidebar.subheader("Selecione o Diagrama")
            display_names = [os.path.splitext(f)[0] for f in diagram_files]
            selected_display_name = st.sidebar.selectbox("Diagramas Disponíveis", options=display_names, label_visibility="collapsed")
            
            selected_file = f"{selected_display_name}.mmd"
            file_path = os.path.join(diagrams_dir, selected_file)

            with open(file_path, "r", encoding="utf-8") as f:
                mermaid_code = f.read()

            st.subheader(f"Diagrama: {selected_display_name}")
            st_mermaid(mermaid_code, height="800px")

# --- Modo: Gerar com IA ---
elif app_mode == 'Gerar com IA':
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
