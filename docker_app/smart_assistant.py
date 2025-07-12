from strands import Agent, tool
from real_time_data import enhance_query_with_realtime
from performance_cache import get_cached_response, cache_response

class SmartAssistant:
    def __init__(self, name, system_prompt, tools=None):
        self.name = name
        self.system_prompt = system_prompt
        self.tools = tools or []
        self._agent = None
    
    @property
    def agent(self):
        if not self._agent:
            self._agent = Agent(system_prompt=self.system_prompt, tools=self.tools)
        return self._agent
    
    def __call__(self, query):
        # Check cache
        cached = get_cached_response(query, self.name)
        if cached:
            return f"{cached}\n\n*[Cached]*"
        
        # Enhance with real-time data
        enhanced_query = enhance_query_with_realtime(query, self.name)
        
        # Process
        try:
            response = str(self.agent(enhanced_query))
            cache_response(query, self.name, response)
            return response
        except Exception as e:
            return f"Error in {self.name}: {str(e)}"

# Domain definitions
DOMAINS = {
    'math': "Expert mathematician for calculations and problem solving",
    'aws': "AWS cloud architecture and best practices expert", 
    'crypto': "Cryptocurrency market analysis and blockchain expert",
    'research': "Real-time web research and information gathering expert",
    'finance': "Financial analysis and business finance expert",
    'legal': "Louisiana business law and legal compliance expert"
}

# Create consolidated assistants
assistants = {name: SmartAssistant(name, prompt) for name, prompt in DOMAINS.items()}

@tool
def math_assistant(query: str) -> str:
    return assistants['math'](query)

@tool  
def aws_assistant(query: str) -> str:
    return assistants['aws'](query)

@tool
def cryptocurrency_assistant(query: str) -> str:
    return assistants['crypto'](query)

@tool
def research_assistant(query: str) -> str:
    return assistants['research'](query)

@tool
def financial_assistant(query: str) -> str:
    return assistants['finance'](query)

@tool
def louisiana_legal_assistant(query: str) -> str:
    return assistants['legal'](query)