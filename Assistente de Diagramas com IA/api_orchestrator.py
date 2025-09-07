import os
import json
import asyncio
from typing import Dict, List, Any, Optional
from chroma_manager import ChromaManager
import streamlit as st

class APIOrchestrator:
    """
    Orquestrador automático que gerencia a leitura do grafo de conhecimento,
    sincronização com ChromaDB e análise semântica profunda dos dados.
    """
    
    def __init__(self, base_dir: str, api_model_endpoint: Optional[str] = None):
        self.base_dir = base_dir
        self.kg_path = os.path.join(base_dir, 'knowledge_graph.json')
        self.chroma_manager = ChromaManager(base_dir)
        self.api_model_endpoint = api_model_endpoint
        self.knowledge_graph = None
        self.semantic_insights = {}
        
    async def initialize_system(self) -> Dict[str, Any]:
        """
        Sequência automática de inicialização:
        1. Lê o knowledge graph para visão inicial
        2. Sincroniza ChromaDB se necessário
        3. Executa análise semântica profunda dos nós
        """
        initialization_report = {
            "status": "initializing",
            "steps": [],
            "insights": {},
            "errors": []
        }
        
        try:
            # Passo 1: Leitura inicial do grafo de conhecimento
            step1_result = await self._read_knowledge_graph()
            initialization_report["steps"].append(step1_result)
            
            # Passo 2: Sincronização automática do ChromaDB
            step2_result = await self._sync_chromadb()
            initialization_report["steps"].append(step2_result)
            
            # Passo 3: Análise semântica profunda
            step3_result = await self._perform_semantic_analysis()
            initialization_report["steps"].append(step3_result)
            initialization_report["insights"] = self.semantic_insights
            
            initialization_report["status"] = "completed"
            
        except Exception as e:
            initialization_report["status"] = "error"
            initialization_report["errors"].append(str(e))
            
        return initialization_report
    
    async def _read_knowledge_graph(self) -> Dict[str, Any]:
        """Lê e analisa o grafo de conhecimento para visão inicial"""
        step_result = {
            "step": "knowledge_graph_reading",
            "status": "running",
            "details": {}
        }
        
        try:
            with open(self.kg_path, 'r', encoding='utf-8') as f:
                self.knowledge_graph = json.load(f)
            
            # Análise inicial dos componentes
            nodes_by_type = {}
            for node in self.knowledge_graph.get('nodes', []):
                node_type = node.get('type', 'unknown')
                if node_type not in nodes_by_type:
                    nodes_by_type[node_type] = []
                nodes_by_type[node_type].append(node)
            
            step_result.update({
                "status": "completed",
                "details": {
                    "total_nodes": len(self.knowledge_graph.get('nodes', [])),
                    "total_edges": len(self.knowledge_graph.get('edges', [])),
                    "nodes_by_type": {k: len(v) for k, v in nodes_by_type.items()},
                    "architecture_overview": self._generate_architecture_overview(nodes_by_type)
                }
            })
            
        except Exception as e:
            step_result.update({
                "status": "error",
                "error": str(e)
            })
            
        return step_result
    
    async def _sync_chromadb(self) -> Dict[str, Any]:
        """Sincroniza automaticamente o ChromaDB"""
        step_result = {
            "step": "chromadb_sync",
            "status": "running",
            "details": {}
        }
        
        try:
            sync_needed = self.chroma_manager.is_sync_needed()
            
            if sync_needed:
                self.chroma_manager.run_ingestion()
                step_result["details"]["action"] = "synchronized"
                step_result["details"]["reason"] = "knowledge graph was updated"
            else:
                step_result["details"]["action"] = "skipped"
                step_result["details"]["reason"] = "already synchronized"
            
            # Verificar status do banco
            collection = self.chroma_manager.collection
            results = collection.get()
            step_result["details"]["total_items"] = len(results.get('ids', []))
            
            step_result["status"] = "completed"
            
        except Exception as e:
            step_result.update({
                "status": "error",
                "error": str(e)
            })
            
        return step_result
    
    async def _perform_semantic_analysis(self) -> Dict[str, Any]:
        """Executa análise semântica profunda dos nós"""
        step_result = {
            "step": "semantic_analysis",
            "status": "running",
            "details": {}
        }
        
        try:
            # Identificar nós novos ou modificados
            new_nodes = self._identify_new_nodes()
            
            # Análise semântica para cada tipo de nó
            semantic_analysis = {}
            
            for node in self.knowledge_graph.get('nodes', []):
                node_id = node.get('id')
                node_type = node.get('type')
                
                # Consulta semântica específica para o nó
                semantic_query = self._generate_semantic_query(node)
                results = self.chroma_manager.semantic_query(semantic_query, n_results=3)
                
                # Análise de relacionamentos semânticos
                related_concepts = self._analyze_semantic_relationships(node, results)
                
                semantic_analysis[node_id] = {
                    "type": node_type,
                    "semantic_query": semantic_query,
                    "related_concepts": related_concepts,
                    "semantic_score": self._calculate_semantic_score(results),
                    "is_new": node_id in new_nodes
                }
            
            self.semantic_insights = semantic_analysis
            
            step_result.update({
                "status": "completed",
                "details": {
                    "analyzed_nodes": len(semantic_analysis),
                    "new_nodes_count": len(new_nodes),
                    "semantic_depth_score": self._calculate_overall_semantic_depth()
                }
            })
            
        except Exception as e:
            step_result.update({
                "status": "error",
                "error": str(e)
            })
            
        return step_result
    
    def _generate_architecture_overview(self, nodes_by_type: Dict[str, List]) -> Dict[str, Any]:
        """Gera uma visão geral da arquitetura"""
        return {
            "core_components": len(nodes_by_type.get('agent', [])) + len(nodes_by_type.get('orchestrator', [])),
            "data_objects": len(nodes_by_type.get('data_object', [])),
            "knowledge_sources": len(nodes_by_type.get('knowledge_source', [])),
            "external_services": len(nodes_by_type.get('external_service', [])),
            "ui_components": len(nodes_by_type.get('ui_component', [])),
            "databases": len(nodes_by_type.get('database', [])),
            "scripts": len(nodes_by_type.get('script', []))
        }
    
    def _identify_new_nodes(self) -> List[str]:
        """Identifica nós novos baseado em timestamps ou outras heurísticas"""
        # Por enquanto, considera nós com ChromaDB como novos
        new_node_keywords = ['chroma', 'semantic', 'vector', 'search']
        new_nodes = []
        
        for node in self.knowledge_graph.get('nodes', []):
            node_id = node.get('id', '').lower()
            node_label = node.get('label', '').lower()
            
            if any(keyword in node_id or keyword in node_label for keyword in new_node_keywords):
                new_nodes.append(node.get('id'))
                
        return new_nodes
    
    def _generate_semantic_query(self, node: Dict[str, Any]) -> str:
        """Gera consulta semântica específica para um nó"""
        node_type = node.get('type', '')
        node_label = node.get('label', '')
        
        query_templates = {
            'agent': f"Como o {node_label} funciona e qual sua responsabilidade?",
            'database': f"Qual o propósito do {node_label} e que dados armazena?",
            'module': f"Que funcionalidades o {node_label} oferece?",
            'ui_component': f"Que recursos e interações o {node_label} proporciona?",
            'script': f"Qual a função do {node_label} no sistema?",
            'orchestrator': f"Como o {node_label} coordena outros componentes?"
        }
        
        return query_templates.get(node_type, f"Explique o papel do {node_label} na arquitetura")
    
    def _analyze_semantic_relationships(self, node: Dict[str, Any], results: Dict[str, Any]) -> List[str]:
        """Analisa relacionamentos semânticos baseado nos resultados da consulta"""
        if not results or not results.get('documents') or not results['documents'][0]:
            return []
        
        related_concepts = []
        for doc in results['documents'][0]:
            # Extrai conceitos relacionados do documento
            if 'agente' in doc.lower():
                related_concepts.append('agent_interaction')
            if 'dados' in doc.lower() or 'database' in doc.lower():
                related_concepts.append('data_management')
            if 'interface' in doc.lower() or 'ui' in doc.lower():
                related_concepts.append('user_interface')
                
        return list(set(related_concepts))
    
    def _calculate_semantic_score(self, results: Dict[str, Any]) -> float:
        """Calcula um score semântico baseado na qualidade dos resultados"""
        if not results or not results.get('documents') or not results['documents'][0]:
            return 0.0
        
        # Score baseado no número e qualidade dos resultados
        num_results = len(results['documents'][0])
        return min(num_results * 0.3, 1.0)
    
    def _calculate_overall_semantic_depth(self) -> float:
        """Calcula a profundidade semântica geral do sistema"""
        if not self.semantic_insights:
            return 0.0
        
        total_score = sum(insight.get('semantic_score', 0) for insight in self.semantic_insights.values())
        return total_score / len(self.semantic_insights)
    
    def get_semantic_insights_for_node(self, node_id: str) -> Optional[Dict[str, Any]]:
        """Retorna insights semânticos para um nó específico"""
        return self.semantic_insights.get(node_id)
    
    def get_architecture_summary(self) -> Dict[str, Any]:
        """Retorna um resumo da arquitetura com insights semânticos"""
        if not self.knowledge_graph:
            return {"error": "Knowledge graph not loaded"}
        
        return {
            "total_components": len(self.knowledge_graph.get('nodes', [])),
            "semantic_depth": self._calculate_overall_semantic_depth(),
            "new_components": len([n for n in self.semantic_insights.values() if n.get('is_new', False)]),
            "high_connectivity_nodes": self._identify_high_connectivity_nodes()
        }
    
    def _identify_high_connectivity_nodes(self) -> List[str]:
        """Identifica nós com alta conectividade no grafo"""
        edge_count = {}
        
        for edge in self.knowledge_graph.get('edges', []):
            source = edge.get('source')
            target = edge.get('target')
            
            edge_count[source] = edge_count.get(source, 0) + 1
            edge_count[target] = edge_count.get(target, 0) + 1
        
        # Retorna nós com mais de 3 conexões
        return [node for node, count in edge_count.items() if count > 3]
