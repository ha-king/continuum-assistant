"""
Aviation Assistant
Specialized assistant for aviation, flight data, and FAA information
"""

from strands import Agent, tool
from aviation_data_access import enhance_query_with_aviation_data
from realtime_data_access import enhance_query_with_realtime

AVIATION_SYSTEM_PROMPT = """
You have LIVE flight position data from FlightTracker.com API.

For N-number queries: Use the exact flight position data provided in your context.

NEVER say you lack access to real-time data.
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
        
        # Also add general real-time context
        fully_enhanced = enhance_query_with_realtime(aviation_enhanced, "aviation")
        
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