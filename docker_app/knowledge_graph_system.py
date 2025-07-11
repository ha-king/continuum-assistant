import json
import boto3
from datetime import datetime
import networkx as nx
import matplotlib.pyplot as plt
import io
import base64

class KnowledgeGraphSystem:
    def __init__(self):
        self.bedrock = boto3.client('bedrock-runtime', region_name='us-west-2')
        self.graph = nx.DiGraph()
        self.entity_types = {
            'PERSON': '👤',
            'COMPANY': '🏢',
            'TECHNOLOGY': '💻',
            'MARKET': '📈',
            'CURRENCY': '💰',
            'LOCATION': '📍',
            'EVENT': '📅',
            'CONCEPT': '💡'
        }
        
    def extract_entities_and_relationships(self, text):
        """Extract entities and relationships from text"""
        try:
            extraction_prompt = f"""
            Extract entities and relationships from this text:
            "{text}"
            
            Return JSON format:
            {{
                "entities": [
                    {{"name": "entity_name", "type": "PERSON|COMPANY|TECHNOLOGY|MARKET|CURRENCY|LOCATION|EVENT|CONCEPT", "description": "brief description"}}
                ],
                "relationships": [
                    {{"source": "entity1", "target": "entity2", "relationship": "relationship_type", "strength": 0.8}}
                ]
            }}
            
            Focus on business, financial, and technological entities.
            """
            
            response = self.bedrock.invoke_model(
                modelId="anthropic.claude-3-5-sonnet-20241022-v1:0",
                body=json.dumps({
                    "messages": [{"role": "user", "content": extraction_prompt}],
                    "max_tokens": 500,
                    "temperature": 0.1
                })
            )
            
            result = json.loads(response['body'].read())
            content = result.get('content', [{}])[0].get('text', '{}')
            
            # Extract JSON from response
            try:
                start_idx = content.find('{')
                end_idx = content.rfind('}') + 1
                json_str = content[start_idx:end_idx]
                return json.loads(json_str)
            except:
                return {"entities": [], "relationships": []}
                
        except Exception as e:
            print(f"Entity extraction error: {str(e)}")
            return {"entities": [], "relationships": []}
    
    def add_to_knowledge_graph(self, entities_data):
        """Add entities and relationships to knowledge graph"""
        try:
            # Add entities
            for entity in entities_data.get('entities', []):
                self.graph.add_node(
                    entity['name'],
                    type=entity['type'],
                    description=entity.get('description', ''),
                    added_at=datetime.now().isoformat()
                )
            
            # Add relationships
            for rel in entities_data.get('relationships', []):
                self.graph.add_edge(
                    rel['source'],
                    rel['target'],
                    relationship=rel['relationship'],
                    strength=rel.get('strength', 0.5),
                    added_at=datetime.now().isoformat()
                )
                
        except Exception as e:
            print(f"Knowledge graph update error: {str(e)}")
    
    def find_connections(self, entity1, entity2, max_depth=3):
        """Find connections between two entities"""
        try:
            if entity1 not in self.graph or entity2 not in self.graph:
                return f"One or both entities not found in knowledge graph"
            
            # Find shortest path
            try:
                path = nx.shortest_path(self.graph, entity1, entity2)
                path_length = len(path) - 1
                
                connection_info = f"🔗 **Connection Path ({path_length} steps):**\n\n"
                
                for i in range(len(path) - 1):
                    source = path[i]
                    target = path[i + 1]
                    
                    # Get relationship info
                    edge_data = self.graph.get_edge_data(source, target, {})
                    relationship = edge_data.get('relationship', 'connected to')
                    
                    # Get entity types
                    source_type = self.graph.nodes[source].get('type', 'CONCEPT')
                    target_type = self.graph.nodes[target].get('type', 'CONCEPT')
                    
                    source_emoji = self.entity_types.get(source_type, '💡')
                    target_emoji = self.entity_types.get(target_type, '💡')
                    
                    connection_info += f"{source_emoji} **{source}** → *{relationship}* → {target_emoji} **{target}**\n"
                
                return connection_info
                
            except nx.NetworkXNoPath:
                return f"No connection found between {entity1} and {entity2}"
                
        except Exception as e:
            return f"Connection search error: {str(e)}"
    
    def get_entity_network(self, entity, depth=2):
        """Get network of connections for an entity"""
        try:
            if entity not in self.graph:
                return f"Entity '{entity}' not found in knowledge graph"
            
            # Get subgraph within specified depth
            subgraph_nodes = set([entity])
            current_nodes = set([entity])
            
            for _ in range(depth):
                next_nodes = set()
                for node in current_nodes:
                    # Add neighbors
                    neighbors = set(self.graph.neighbors(node)) | set(self.graph.predecessors(node))
                    next_nodes.update(neighbors)
                
                subgraph_nodes.update(next_nodes)
                current_nodes = next_nodes
            
            subgraph = self.graph.subgraph(subgraph_nodes)
            
            network_info = f"🕸️ **Network for {entity}:**\n\n"
            network_info += f"**Connected Entities ({len(subgraph_nodes) - 1}):**\n"
            
            # Group by entity type
            by_type = {}
            for node in subgraph_nodes:
                if node != entity:
                    node_type = self.graph.nodes[node].get('type', 'CONCEPT')
                    if node_type not in by_type:
                        by_type[node_type] = []
                    by_type[node_type].append(node)
            
            for entity_type, entities in by_type.items():
                emoji = self.entity_types.get(entity_type, '💡')
                network_info += f"\n{emoji} **{entity_type}**: {', '.join(entities)}\n"
            
            return network_info
            
        except Exception as e:
            return f"Network analysis error: {str(e)}"
    
    def analyze_knowledge_patterns(self):
        """Analyze patterns in the knowledge graph"""
        try:
            if len(self.graph.nodes) == 0:
                return "Knowledge graph is empty"
            
            analysis = f"📊 **Knowledge Graph Analysis:**\n\n"
            analysis += f"**Entities**: {len(self.graph.nodes)}\n"
            analysis += f"**Relationships**: {len(self.graph.edges)}\n"
            analysis += f"**Connected Components**: {nx.number_connected_components(self.graph.to_undirected())}\n\n"
            
            # Most connected entities
            degree_centrality = nx.degree_centrality(self.graph)
            top_entities = sorted(degree_centrality.items(), key=lambda x: x[1], reverse=True)[:5]
            
            analysis += "**Most Connected Entities:**\n"
            for entity, centrality in top_entities:
                entity_type = self.graph.nodes[entity].get('type', 'CONCEPT')
                emoji = self.entity_types.get(entity_type, '💡')
                analysis += f"{emoji} {entity} (connections: {centrality:.2f})\n"
            
            return analysis
            
        except Exception as e:
            return f"Pattern analysis error: {str(e)}"
    
    def suggest_related_queries(self, current_query):
        """Suggest related queries based on knowledge graph"""
        try:
            # Extract entities from current query
            entities_data = self.extract_entities_and_relationships(current_query)
            
            if not entities_data.get('entities'):
                return "No related suggestions available"
            
            suggestions = f"🔍 **Related Query Suggestions:**\n\n"
            
            # Find related entities for each entity in the query
            for entity_info in entities_data['entities'][:2]:  # Limit to first 2 entities
                entity_name = entity_info['name']
                
                if entity_name in self.graph:
                    # Get connected entities
                    connected = list(self.graph.neighbors(entity_name))[:3]
                    
                    for connected_entity in connected:
                        relationship = self.graph.get_edge_data(entity_name, connected_entity, {})
                        rel_type = relationship.get('relationship', 'related to')
                        
                        suggestions += f"• How is {entity_name} {rel_type} {connected_entity}?\n"
                        suggestions += f"• What's the latest on {connected_entity}?\n"
            
            return suggestions
            
        except Exception as e:
            return f"Suggestion error: {str(e)}"

# Global instance
knowledge_graph = KnowledgeGraphSystem()

def process_text_for_knowledge_graph(text):
    """Process text and add to knowledge graph"""
    entities_data = knowledge_graph.extract_entities_and_relationships(text)
    knowledge_graph.add_to_knowledge_graph(entities_data)
    return f"Added {len(entities_data.get('entities', []))} entities and {len(entities_data.get('relationships', []))} relationships to knowledge graph"

def find_entity_connections(entity1, entity2):
    """Find connections between entities"""
    return knowledge_graph.find_connections(entity1, entity2)

def get_entity_network(entity):
    """Get entity network"""
    return knowledge_graph.get_entity_network(entity)

def analyze_knowledge_patterns():
    """Analyze knowledge graph patterns"""
    return knowledge_graph.analyze_knowledge_patterns()

def get_related_suggestions(query):
    """Get related query suggestions"""
    return knowledge_graph.suggest_related_queries(query)