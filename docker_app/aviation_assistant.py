"""
Aviation Assistant
Specialized assistant for aviation, flight data, and FAA information
"""

from strands import Agent, tool
from aviation_data_access import enhance_query_with_aviation_data
from aviation_knowledge import enhance_with_aviation_knowledge
from aircraft_registry import get_registration
from aircraft_web_search import search_aircraft
from aviation_knowledge import enhance_with_aviation_knowledge
from realtime_data_access import enhance_query_with_realtime

AVIATION_SYSTEM_PROMPT = """
You are an aviation expert with access to multiple data sources:

1. FlightRadar24 API - For real-time aircraft position data
2. FAA data - For regulations, NOTAMs, and airport information
3. Aviation weather - For METARs, TAFs, and conditions
4. Flight delays - For current airport operations

For N-number queries (like N628TS): Use the exact flight position data provided.
For general aviation questions: Provide expert guidance on regulations, operations, aircraft, airports, etc.

Always use the data provided in your context when available.
"""

@tool
def aviation_assistant(query: str) -> str:
    """
    Process aviation-related queries with live flight data and FAA information.
    
    Args:
        query: An aviation question or flight information request
        
    Returns:
        Expert aviation guidance with current data
    """
    try:
        print("Routed to Aviation Assistant")
        
        # Enhance query with aviation-specific data
        aviation_enhanced = enhance_query_with_aviation_data(query)
        
        # Add aviation knowledge for general questions
        knowledge_enhanced = aviation_enhanced + "\n\n" + enhance_with_aviation_knowledge(query)
        
        # Add web search results for aircraft
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
        
        # Also add general real-time context
        fully_enhanced = enhance_query_with_realtime(knowledge_enhanced, "aviation")
        
        # Create aviation agent
        aviation_agent = Agent(
            system_prompt=AVIATION_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = aviation_agent(fully_enhanced)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the aviation query. Please provide more specific details."
            
    except Exception as e:
        return f"Aviation analysis error: {str(e)}"