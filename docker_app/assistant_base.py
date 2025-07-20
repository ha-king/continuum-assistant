"""
Assistant Base Module
Provides common functionality for all assistants
"""

from typing import Optional, Dict, Any
from shared_knowledge import store_knowledge, retrieve_knowledge, learn_from_interaction

class AssistantBase:
    """Base class for all assistants with shared knowledge capabilities"""
    
    def __init__(self, assistant_name: str):
        self.assistant_name = assistant_name
    
    def process_query(self, query: str) -> str:
        """Process a query with knowledge base integration"""
        # First check knowledge base
        kb_result = self.check_knowledge_base(query)
        
        # If found in knowledge base, use that
        if kb_result:
            return f"From knowledge base: {kb_result}"
        
        # Otherwise, process normally
        result = self.process_normally(query)
        
        # Store result in knowledge base
        self.store_in_knowledge_base(query, result)
        
        return result
    
    def check_knowledge_base(self, query: str) -> Optional[str]:
        """Check if query can be answered from knowledge base"""
        try:
            # Check knowledge base for exact query
            kb_result = retrieve_knowledge(query)
            if kb_result and 'data' in kb_result:
                return kb_result['data']
            
            # Check for topic matches
            topics = self._extract_topics(query)
            for topic in topics:
                kb_result = retrieve_knowledge(topic)
                if kb_result and 'data' in kb_result:
                    return kb_result['data']
            
            return None
        except:
            return None
    
    def store_in_knowledge_base(self, query: str, result: str) -> None:
        """Store query result in knowledge base"""
        try:
            # Store full query-result pair
            store_knowledge(query, result, self.assistant_name)
            
            # Also store for extracted topics
            topics = self._extract_topics(query)
            for topic in topics:
                store_knowledge(topic, result, self.assistant_name)
            
            # Learn from interaction
            learn_from_interaction(query, result)
        except:
            pass
    
    def _extract_topics(self, query: str) -> list:
        """Extract potential topics from query"""
        topics = []
        query_lower = query.lower()
        
        # Extract words that might be topics
        words = query_lower.split()
        for i in range(len(words)):
            # Single words (skip common words)
            if len(words[i]) >= 4 and words[i] not in ["what", "where", "when", "which", "whose", "about", "there"]:
                topics.append(words[i])
            
            # Word pairs
            if i < len(words) - 1:
                word_pair = f"{words[i]} {words[i+1]}"
                topics.append(word_pair)
        
        return topics
    
    def process_normally(self, query: str) -> str:
        """Process query normally (to be implemented by subclasses)"""
        raise NotImplementedError("Subclasses must implement process_normally")