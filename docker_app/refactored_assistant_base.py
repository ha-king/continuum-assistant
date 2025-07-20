"""
Refactored Assistant Base
Provides a unified base class for all assistants
"""

from typing import Optional, Dict, Any, List
from shared_knowledge import store_knowledge, retrieve_knowledge, learn_from_interaction
from realtime_data_access import enhance_query_with_realtime

class AssistantBase:
    """Base class for all assistants with shared functionality"""
    
    def __init__(self, name: str, system_prompt: str):
        self.name = name
        self.system_prompt = system_prompt
    
    def __call__(self, query: str) -> str:
        """Process a query with knowledge base integration"""
        # Step 1: Check knowledge base first
        kb_result = self.check_knowledge_base(query)
        if kb_result:
            return f"From knowledge base: {kb_result}"
        
        # Step 2: Enhance query with real-time data
        enhanced_query = self.enhance_query(query)
        
        # Step 3: Process with LLM
        response = self.process_with_llm(enhanced_query)
        
        # Step 4: Store in knowledge base
        self.store_in_knowledge_base(query, response)
        
        return response
    
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
    
    def enhance_query(self, query: str) -> str:
        """Enhance query with real-time data"""
        try:
            # Add real-time context
            enhanced = enhance_query_with_realtime(query, self.name)
            return enhanced
        except:
            return query
    
    def process_with_llm(self, query: str) -> str:
        """Process query with LLM"""
        # This should be implemented by subclasses
        raise NotImplementedError("Subclasses must implement process_with_llm")
    
    def store_in_knowledge_base(self, query: str, response: str) -> None:
        """Store query result in knowledge base"""
        try:
            # Store full query-result pair
            store_knowledge(query, response, self.name)
            
            # Also store for extracted topics
            topics = self._extract_topics(query)
            for topic in topics:
                store_knowledge(topic, response, self.name)
            
            # Learn from interaction
            learn_from_interaction(query, response)
        except:
            pass
    
    def _extract_topics(self, query: str) -> List[str]:
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