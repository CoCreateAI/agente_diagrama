#!/usr/bin/env python3
"""
Script to test the enhanced ChromaDB system with force re-ingestion
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'Assistente de Diagramas com IA'))

from chroma_manager import ChromaManager

def main():
    print("🔄 Testing ChromaDB Enhanced System")
    print("=" * 50)
    
    # Initialize ChromaManager
    base_dir = os.path.dirname(__file__)
    chroma_manager = ChromaManager(base_dir)
    
    print("📊 Current ChromaDB Status:")
    try:
        all_data = chroma_manager.get_all_data()
        print(f"   Total items: {all_data['total_items']}")
    except Exception as e:
        print(f"   Error getting current data: {e}")
    
    print("\n🗑️ Forcing complete re-ingestion...")
    try:
        chroma_manager.force_reingest()
        print("✅ Re-ingestion completed successfully!")
    except Exception as e:
        print(f"❌ Error during re-ingestion: {e}")
        return
    
    print("\n📈 New ChromaDB Status:")
    try:
        all_data = chroma_manager.get_all_data()
        print(f"   Total items: {all_data['total_items']}")
        
        # Test semantic query with enhanced data
        print("\n🔍 Testing semantic query with enhanced summaries:")
        results = chroma_manager.semantic_query("ChromaDB manager funcionalidades", n_results=3)
        
        if results and results.get('documents') and results['documents'][0]:
            for i, doc in enumerate(results['documents'][0]):
                print(f"\n   Result {i+1}:")
                print(f"   📄 Document: {doc[:100]}...")
                
                metadata = results['metadatas'][0][i]
                print(f"   🏷️ Type: {metadata.get('type', 'N/A')}")
                print(f"   🆔 ID: {metadata.get('id', 'N/A')}")
                if 'summary' in metadata and metadata['summary']:
                    print(f"   📝 Summary: {metadata['summary'][:80]}...")
        else:
            print("   ⚠️ No results found")
            
    except Exception as e:
        print(f"   Error testing enhanced system: {e}")
    
    print("\n✨ Enhanced ChromaDB system test completed!")

if __name__ == "__main__":
    main()
