"""
Refactored Knowledge System
Consolidates duplicate knowledge storage methods
"""

from typing import Optional, Dict, List, Any
from datetime import datetime
import re
import json

class KnowledgeSystem:
    """Unified knowledge system for all assistants"""
    
    def __init__(self):
        self.local_cache = {}
        self.cache_time = {}
        self.cache_duration = 3600  # 1 hour
    
    def store(self, topic: str, data: Any, source: str = "assistant") -> bool:
        """Store knowledge in the knowledge base"""
        try:
            # Normalize topic
            topic_key = self._normalize_topic(topic)
            
            # Format data for storage
            timestamp = datetime.now().isoformat()
            knowledge_entry = {
                "data": data,
                "source": source,
                "timestamp": timestamp
            }
            
            # Store in knowledge base
            from strands import Agent
            from strands_tools import memory, use_llm
            
            # Create agent with memory access
            agent = Agent(tools=[memory, use_llm])
            
            # Store in knowledge base
            agent.tool.memory(
                action="store",
                content=f"TOPIC: {topic}\nDATA: {json.dumps(knowledge_entry)}\nTIMESTAMP: {timestamp}"
            )
            
            # Also update local cache
            self.local_cache[topic_key] = knowledge_entry
            self.cache_time[topic_key] = datetime.now().timestamp()
            
            return True
        except Exception as e:
            # Fall back to local storage
            try:
                topic_key = self._normalize_topic(topic)
                knowledge_entry = {
                    "data": data,
                    "source": source,
                    "timestamp": datetime.now().isoformat()
                }
                self.local_cache[topic_key] = knowledge_entry
                self.cache_time[topic_key] = datetime.now().timestamp()
                return True
            except:
                return False
    
    def retrieve(self, topic: str, min_score: float = 0.7) -> Optional[Dict]:
        """Retrieve knowledge from the knowledge base"""
        try:
            # Normalize topic
            topic_key = self._normalize_topic(topic)
            
            # Check local cache first
            if topic_key in self.local_cache:
                # Check if cache is still valid
                if datetime.now().timestamp() - self.cache_time.get(topic_key, 0) < self.cache_duration:
                    return self.local_cache[topic_key]
            
            # Query knowledge base
            from strands import Agent
            from strands_tools import memory, use_llm
            
            # Create agent with memory access
            agent = Agent(tools=[memory, use_llm])
            
            # Query the knowledge base
            kb_results = agent.tool.memory(
                action="retrieve",
                query=f"TOPIC: {topic}",
                min_score=min_score,
                max_results=3
            )
            
            if kb_results:
                # Parse results to extract knowledge entries
                results_str = str(kb_results)
                
                # Look for JSON data
                json_pattern = r'DATA: ({.*?})'
                json_matches = re.findall(json_pattern, results_str)
                
                if json_matches:
                    for json_str in json_matches:
                        try:
                            entry = json.loads(json_str)
                            # Update local cache
                            self.local_cache[topic_key] = entry
                            self.cache_time[topic_key] = datetime.now().timestamp()
                            return entry
                        except:
                            continue
            
            return None
        except:
            # Fall back to local cache even if expired
            if topic_key in self.local_cache:
                return self.local_cache[topic_key]
            return None
    
    def learn(self, query: str, response: str) -> None:
        """Learn from query-response interactions"""
        try:
            # Extract potential topics from query
            topics = self._extract_topics(query)
            
            # Store response for each identified topic
            for topic in topics:
                self.store(topic, response, "interaction")
        except:
            pass
    
    def _normalize_topic(self, topic: str) -> str:
        """Normalize topic for consistent lookup"""
        return topic.lower().strip()
    
    def _extract_topics(self, text: str) -> List[str]:
        """Extract potential topics from text"""
        topics = []
        text_lower = text.lower()
        
        # Extract named entities (simplified approach)
        words = text_lower.split()
        for i in range(len(words)):
            # Single words that might be topics
            if len(words[i]) >= 4 and words[i] not in ["what", "where", "when", "which", "whose", "about", "there"]:
                topics.append(words[i])
            
            # Word pairs
            if i < len(words) - 1:
                word_pair = f"{words[i]} {words[i+1]}"
                topics.append(word_pair)
        
        return topics

# Global instance
knowledge_system = KnowledgeSystem()

# Simplified API
def store(topic: str, data: Any, source: str = "assistant") -> bool:
    """Store knowledge in the knowledge base"""
    return knowledge_system.store(topic, data, source)

def retrieve(topic: str, min_score: float = 0.7) -> Optional[Dict]:
    """Retrieve knowledge from the knowledge base"""
    return knowledge_system.retrieve(topic, min_score)

def learn(query: str, response: str) -> None:
    """Learn from query-response interactions"""
    knowledge_system.learn(query, response)