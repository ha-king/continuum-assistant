from strands import Agent
from performance_cache import get_cached_response, cache_response
import asyncio
from concurrent.futures import ThreadPoolExecutor

class AssistantManager:
    def __init__(self):
        self.executor = ThreadPoolExecutor(max_workers=4)
        self.assistants = {}
    
    def get_assistant(self, assistant_type, system_prompt):
        if assistant_type not in self.assistants:
            self.assistants[assistant_type] = Agent(system_prompt=system_prompt)
        return self.assistants[assistant_type]
    
    async def process_query_async(self, query, assistant_type, system_prompt):
        # Check cache first
        cached = get_cached_response(query, assistant_type)
        if cached:
            return f"{cached}\n\n*[Cached response]*"
        
        # Process in thread pool
        loop = asyncio.get_event_loop()
        agent = self.get_assistant(assistant_type, system_prompt)
        
        try:
            response = await loop.run_in_executor(self.executor, agent, query)
            result = str(response)
            
            # Cache successful responses
            if result and len(result) > 10:
                cache_response(query, assistant_type, result)
            
            return result
        except Exception as e:
            return f"Error: {str(e)}"

# Global manager
assistant_manager = AssistantManager()