"""
Refactored Aviation Assistant
Demonstrates using the refactored base class
"""

from strands import Agent
from refactored_assistant_base import AssistantBase
from aviation_data_access import enhance_query_with_aviation_data
from aviation_knowledge import enhance_with_aviation_knowledge
from aircraft_registry import get_registration
from aircraft_web_search import search_aircraft
from aircraft_learning import learn_from_interaction, get_learned_registration

# Aviation system prompt
AVIATION_SYSTEM_PROMPT = """
You have live FlightRadar24 API data. Use the FLIGHT POSITION data in your context.

For N628TS: Report the exact coordinates, altitude, and speed from the API data provided.
"""

class RefactoredAviationAssistant(AssistantBase):
    """Refactored aviation assistant using base class"""
    
    def __init__(self):
        super().__init__("aviation", AVIATION_SYSTEM_PROMPT)
        self.agent = Agent(system_prompt=AVIATION_SYSTEM_PROMPT)
    
    def enhance_query(self, query: str) -> str:
        """Enhance query with aviation-specific data"""
        try:
            # Enhance with aviation data
            aviation_enhanced = enhance_query_with_aviation_data(query)
            
            # Add aviation knowledge
            knowledge_enhanced = aviation_enhanced + "\n\n" + enhance_with_aviation_knowledge(query)
            
            # Add aircraft web search data
            aircraft_id = None
            
            # Check for N-numbers
            for word in query.split():
                if len(word) >= 4 and word.upper().startswith('N'):
                    aircraft_id = word.upper()
                    break
            
            # If no N-number, check for aircraft names
            if not aircraft_id and ('aircraft' in query.lower() or 'plane' in query.lower() or 'jet' in query.lower()):
                # Extract potential aircraft name
                words = query.lower().split()
                for i in range(len(words)):
                    if words[i] in ['aircraft', 'plane', 'jet'] and i > 0:
                        aircraft_id = words[i-1]  # Use word before aircraft/plane/jet
                        break
            
            # Add web search results if aircraft identified
            if aircraft_id:
                try:
                    search_results = search_aircraft(aircraft_id)
                    if search_results:
                        result_str = "\n\nAIRCRAFT WEB SEARCH:\n"
                        for key, value in search_results.items():
                            if key not in ['url', 'source']:
                                result_str += f"{key}: {value}\n"
                        result_str += f"Source: {search_results.get('source', 'Unknown')} - {search_results.get('url', '')}\n"
                        knowledge_enhanced += result_str
                except:
                    pass
            
            # Add general real-time context
            from realtime_data_access import enhance_query_with_realtime
            fully_enhanced = enhance_query_with_realtime(knowledge_enhanced, "aviation")
            
            return fully_enhanced
        except:
            # Fall back to basic enhancement
            return super().enhance_query(query)
    
    def process_with_llm(self, query: str) -> str:
        """Process query with LLM"""
        try:
            # Use strands agent
            response = self.agent(query)
            return str(response)
        except Exception as e:
            return f"Error processing query: {str(e)}"

# Create global instance
refactored_aviation_assistant = RefactoredAviationAssistant()

def aviation_assistant_refactored(query: str) -> str:
    """Convenience function for aviation assistant"""
    return refactored_aviation_assistant(query)