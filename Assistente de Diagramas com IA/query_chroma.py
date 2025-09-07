import os
import streamlit as st
import chromadb
import pandas as pd

def view_chroma_data():
    """
    A Streamlit app to connect to ChromaDB, retrieve all data from the 
    'knowledge_graph' collection, and display it in interactive tables.
    """
    st.set_page_config(layout="wide")
    st.title("Visualizador de Dados do Knowledge Graph (ChromaDB)")

    # Define paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    db_path = os.path.join(base_dir, 'chroma_db')

    if not os.path.exists(db_path):
        st.error(f"Erro: Banco de dados ChromaDB não encontrado em '{db_path}'.")
        st.warning("Por favor, execute o script de ingestão primeiro.")
        return

    try:
        # 1. Initialize ChromaDB client
        client = chromadb.PersistentClient(path=db_path)
        collection_name = "knowledge_graph"
        collection = client.get_collection(name=collection_name)

        # 2. Retrieve all items from the collection
        results = collection.get()

        if not results or not results['ids']:
            st.warning("A coleção está vazia ou não pôde ser lida.")
            return

        # 3. Separate nodes and edges
        nodes_data = []
        edges_data = []
        for metadata in results['metadatas']:
            if metadata.get('source') == 'nodes':
                nodes_data.append(metadata)
            elif metadata.get('source') == 'edges':
                edges_data.append(metadata)

        # 4. Display data in Streamlit DataFrames
        st.header("Nós do Grafo de Conhecimento")
        if nodes_data:
            node_df = pd.DataFrame(nodes_data)
            st.dataframe(node_df)
        else:
            st.info("Nenhum nó encontrado na coleção.")

        st.header("Arestas do Grafo de Conhecimento")
        if edges_data:
            edge_df = pd.DataFrame(edges_data)
            st.dataframe(edge_df)
        else:
            st.info("Nenhuma aresta encontrada na coleção.")

        st.success(f"Total de itens recuperados: {len(results['ids'])}")

    except Exception as e:
        st.error("Ocorreu um erro durante a consulta.")
        st.exception(e)

if __name__ == "__main__":
    view_chroma_data()
