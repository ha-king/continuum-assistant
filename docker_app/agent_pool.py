from strands import Agent
from threading import Lock

class AgentPool:
    """Shared agent pool to reduce memory usage and initialization overhead"""
    
    def __init__(self):
        self._agents = {}
        self._lock = Lock()
    
    def get_agent(self, system_prompt_hash, system_prompt, tools=None):
        """Get or create agent with caching"""
        with self._lock:
            if system_prompt_hash not in self._agents:
                self._agents[system_prompt_hash] = Agent(
                    system_prompt=system_prompt,
                    tools=tools or []
                )
            return self._agents[system_prompt_hash]
    
    def clear_cache(self):
        """Clear agent cache to free memory"""
        with self._lock:
            self._agents.clear()

# Global agent pool
agent_pool = AgentPool()

def get_cached_agent(system_prompt, tools=None):
    """Get agent from pool with automatic caching"""
    prompt_hash = hash(system_prompt)
    return agent_pool.get_agent(prompt_hash, system_prompt, tools)