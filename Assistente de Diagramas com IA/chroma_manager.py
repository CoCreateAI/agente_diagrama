import os
import json
import hashlib
import chromadb

class ChromaManager:
    """
    Manages all interactions with the ChromaDB database, including initialization,
    synchronization, and querying.
    """
    def __init__(self, base_dir):
        self.base_dir = base_dir
        self.db_path = os.path.join(self.base_dir, 'chroma_db')
        self.kg_path = os.path.join(self.base_dir, 'knowledge_graph.json')
        self.collection_name = "knowledge_graph"
        self.client = chromadb.PersistentClient(path=self.db_path)
        self.collection = self.client.get_or_create_collection(name=self.collection_name)

    def _get_json_hash(self):
        """Calculates the SHA256 hash of the knowledge_graph.json file."""
        with open(self.kg_path, 'rb') as f:
            return hashlib.sha256(f.read()).hexdigest()

    def is_sync_needed(self):
        """Checks if the DB is synchronized with the knowledge_graph.json file."""
        current_hash = self._get_json_hash()
        # Metadata in ChromaDB must be strings, numbers, or booleans
        stored_metadata = self.collection.get(where={"source": "sync_hash"})
        
        if not stored_metadata or not stored_metadata['ids']:
            return True # No hash stored, sync is needed

        stored_hash = stored_metadata['metadatas'][0].get('hash')
        return stored_hash != current_hash

    def run_ingestion(self):
        """Clears and ingests data from knowledge_graph.json into ChromaDB."""
        print("--- Running ChromaDB Ingestion --- ")
        # Clear existing collection
        self.client.delete_collection(name=self.collection_name)
        self.collection = self.client.create_collection(name=self.collection_name)

        # Ingest nodes and edges
        with open(self.kg_path, 'r', encoding='utf-8') as f:
            kg_data = json.load(f)
        
        self._ingest_items(kg_data.get('nodes', []), 'nodes')
        self._ingest_items(kg_data.get('edges', []), 'edges')

        # Store the new hash
        new_hash = self._get_json_hash()
        self.collection.add(
            ids=["sync_hash_id"],
            metadatas=[{"source": "sync_hash", "hash": new_hash}]
        )
        print("--- Ingestion Complete ---")

    def _ingest_items(self, items, item_type):
        """Helper function to ingest a list of nodes or edges."""
        if not items:
            print(f"No {item_type} to ingest.")
            return

        docs, metadatas, ids = [], [], []
        for i, item in enumerate(items):
            if item_type == 'nodes':
                summary = item.get('summary', '')
                doc = f"ID: {item.get('id', '')}, Tipo: {item.get('type', '')}, Label: {item.get('label', '')}"
                if summary:
                    doc += f", Resumo: {summary}"
                metadatas.append({
                    'id': item.get('id', ''),
                    'type': item.get('type', ''),
                    'label': item.get('label', ''),
                    'summary': summary,
                    'source': 'node'
                })
                ids.append(f"node_{item.get('id', '')}")
            else: # edges
                description = item.get('description', '')
                doc = f"Edge from '{item.get('source')}' to '{item.get('target')}' labeled '{item.get('label', '')}'."
                if description:
                    doc += f" Descrição: {description}"
                ids.append(f"edge_{item.get('source')}_{item.get('target')}_{i}")
                metadatas.append({
                    'source': item.get('source', ''),
                    'target': item.get('target', ''),
                    'label': item.get('label', ''),
                    'description': description,
                    'source_type': 'edge'
                })
            docs.append(doc)

        self.collection.add(documents=docs, metadatas=metadatas, ids=ids)
        print(f"Successfully ingested {len(items)} {item_type}.")

    def semantic_query(self, query_text, n_results=3, include_edges=False):
        """Performs a semantic query against the collection."""
        where_clause = None
        if not include_edges:
            where_clause = {"source": "node"}  # Only search within nodes by default
        
        return self.collection.query(
            query_texts=[query_text],
            n_results=n_results,
            where=where_clause
        )
    
    def get_all_data(self):
        """Retrieves all data from the collection for visualization."""
        try:
            results = self.collection.get()
            return {
                'nodes': [],
                'edges': [],
                'total_items': len(results.get('ids', [])),
                'metadatas': results.get('metadatas', []),
                'documents': results.get('documents', [])
            }
        except Exception as e:
            print(f"Error retrieving data: {e}")
            return {'nodes': [], 'edges': [], 'total_items': 0}

    def force_reingest(self):
        """Force a complete re-ingestion of the knowledge graph data."""
        try:
            # Clear existing collection
            self.client.delete_collection(name=self.collection_name)
            print("Cleared existing ChromaDB collection.")
            
            # Recreate collection
            self.collection = self.client.create_collection(name=self.collection_name)
            print("Recreated ChromaDB collection.")
            
            # Run fresh ingestion
            self.run_ingestion()
            print("Completed forced re-ingestion with updated summaries and descriptions.")
            
        except Exception as e:
            print(f"Error during forced re-ingestion: {e}")
            # Recreate collection if it doesn't exist
            try:
                self.collection = self.client.create_collection(name=self.collection_name)
                self.run_ingestion()
            except Exception as e2:
                print(f"Failed to recover: {e2}")
