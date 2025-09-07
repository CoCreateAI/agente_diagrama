import streamlit as st
import streamlit.components.v1 as components
import json
import os
from pyvis.network import Network

def generate_pyvis_from_kg(kg_path, output_filename='knowledge_graph.html'):
    """Reads a knowledge graph JSON and generates an interactive Pyvis graph."""
    if not os.path.exists(kg_path):
        return None, "Error: knowledge_graph.json not found."

    with open(kg_path, 'r', encoding='utf-8') as f:
        kg_data = json.load(f)

    nodes = kg_data.get('nodes', [])
    edges = kg_data.get('edges', [])

    # Define styles
    style_map = {
        'file': {'color': '#f9f9f9', 'shape': 'box', 'borderWidth': 2},
        'agent_file': {'color': '#e0f7fa', 'shape': 'box', 'borderWidth': 2},
        'function': {'color': '#e6f3ff', 'shape': 'dot', 'size': 20},
        'knowledge_source': {'color': '#fff9c4', 'shape': 'database'},
        'external_service': {'color': '#f3e5f5', 'shape': 'hexagon'},
    }

    net = Network(height='800px', width='100%', bgcolor='#222222', font_color='white', notebook=True, directed=True)

    # Add nodes
    for node in nodes:
        node_id = node['id']
        label = node['label']
        node_type = node['type']
        style = style_map.get(node_type, {})
        
        # Make the orchestrator node bigger and more central
        if node_id == 'app.py':
            style['size'] = 40
            style['font'] = {'size': 24}
            net.add_node(node_id, label=label, **style, mass=3)
        else:
            net.add_node(node_id, label=label, **style)

    # Add edges
    for edge in edges:
        net.add_edge(edge['source'], edge['target'], label=edge['label'])

    # Configure physics for a more mind-map like layout
    net.set_options("""
    var options = {
      "physics": {
        "forceAtlas2Based": {
          "gravitationalConstant": -50,
          "centralGravity": 0.01,
          "springLength": 100,
          "springConstant": 0.08
        },
        "minVelocity": 0.75,
        "solver": "forceAtlas2Based"
      }
    }
    """)

    # Generate the HTML file
    net.save_graph(output_filename)
    return output_filename, None

# --- Streamlit App ---
st.set_page_config(page_title="Knowledge Graph Viewer", layout="wide")
st.title("Visualizador do Knowledge Graph do Projeto")

kg_path = 'knowledge_graph.json'
html_file, error = generate_pyvis_from_kg(kg_path)

if error:
    st.error(error)
else:
    with st.spinner("Renderizando o grafo interativo..."):
        with open(html_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
        components.html(source_code, height=800)
