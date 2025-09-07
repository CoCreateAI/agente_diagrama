import os
import json
import chromadb

def ingest_to_chroma():
    """
    Reads the knowledge_graph.json file and ingests its nodes and edges
    into a persistent ChromaDB collection.
    """
    print("--- Starting ChromaDB Ingestion Script ---")

    # Define paths
    base_dir = os.path.dirname(os.path.dirname(__file__))
    kg_path = os.path.join(base_dir, 'knowledge_graph.json')
    db_path = os.path.join(base_dir, 'chroma_db')

    print(f"Knowledge Graph path: {kg_path}")
    print(f"ChromaDB path: {db_path}")

    # Check if knowledge graph file exists
    if not os.path.exists(kg_path):
        print(f"Error: {kg_path} not found.")
        return

    try:
        # 1. Initialize ChromaDB client
        client = chromadb.PersistentClient(path=db_path)

        # 2. Delete the old collection if it exists and create a new one
        collection_name = "knowledge_graph"
        print(f"Deleting old collection '{collection_name}' (if it exists) and creating a new one.")
        client.delete_collection(name=collection_name)
        collection = client.create_collection(name=collection_name)

        # 3. Read the knowledge graph data
        with open(kg_path, 'r', encoding='utf-8') as f:
            kg_data = json.load(f)

        nodes = kg_data.get('nodes', [])
        edges = kg_data.get('edges', [])

        # 4. Prepare and ingest nodes
        if nodes:
            print(f"Ingesting {len(nodes)} nodes...")
            node_documents = []
            node_metadatas = []
            node_ids = []

            for node in nodes:
                doc = f"Node ID: {node['id']}. Type: {node['type']}. Label: {node['label']}."
                node_documents.append(doc)
                node_metadatas.append({"source": "nodes", **node})
                node_ids.append(node['id'])

            collection.add(
                documents=node_documents,
                metadatas=node_metadatas,
                ids=node_ids
            )
            print("Node ingestion complete.")
        else:
            print("No nodes found to ingest.")

        # 5. Prepare and ingest edges
        if edges:
            print(f"Ingesting {len(edges)} edges...")
            edge_documents = []
            edge_metadatas = []
            edge_ids = []

            for i, edge in enumerate(edges):
                doc = f"Relationship from '{edge['source']}' to '{edge['target']}' labeled '{edge['label']}'."
                edge_documents.append(doc)
                edge_metadatas.append({"source": "edges", **edge})
                edge_ids.append(f"edge_{edge['source']}_{edge['target']}_{i}")

            collection.add(
                documents=edge_documents,
                metadatas=edge_metadatas,
                ids=edge_ids
            )
            print("Edge ingestion complete.")
        else:
            print("No edges found to ingest.")

        print(f"\n--- Ingestion Summary ---")
        print(f"Total items in collection '{collection_name}': {collection.count()}")
        print("--------------------------")
        print("\nKnowledge graph successfully ingested into ChromaDB!")

    except Exception as e:
        print(f"\n--- An error occurred during ingestion ---")
        print(f"{e}")
        print("------------------------------------------")

if __name__ == "__main__":
    ingest_to_chroma()
