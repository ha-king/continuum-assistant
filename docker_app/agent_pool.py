from strands import Agent
from threading import Lock
import time

class AgentPool:
    """Shared agent pool to reduce memory usage and initialization overhead"""
    
    def __init__(self, max_size=50):
        self._agents = {}
        self._usage_count = {}
        self._last_used = {}
        self._lock = Lock()
        self._max_size = max_size
    
    def get_agent(self, system_prompt_hash, system_prompt, tools=None):
        """Get or create agent with caching and LRU eviction"""
        with self._lock:
            if system_prompt_hash in self._agents:
                self._usage_count[system_prompt_hash] += 1
                self._last_used[system_prompt_hash] = time.time()
                return self._agents[system_prompt_hash]
            
            # Evict least recently used agent if at capacity
            if len(self._agents) >= self._max_size:
                least_used = min(self._last_used.items(), key=lambda x: x[1])[0]
                del self._agents[least_used]
                del self._usage_count[least_used]
                del self._last_used[least_used]
            
            # Create new agent
            self._agents[system_prompt_hash] = Agent(
                system_prompt=system_prompt,
                tools=tools or []
            )
            self._usage_count[system_prompt_hash] = 1
            self._last_used[system_prompt_hash] = time.time()
            return self._agents[system_prompt_hash]
    
    def clear_cache(self):
        """Clear agent cache to free memory"""
        with self._lock:
            self._agents.clear()
            self._usage_count.clear()
            self._last_used.clear()

# Global agent pool
agent_pool = AgentPool()

def get_cached_agent(system_prompt, tools=None):
    """Get agent from pool with automatic caching"""
    prompt_hash = hash(system_prompt)
    return agent_pool.get_agent(prompt_hash, system_prompt, tools)