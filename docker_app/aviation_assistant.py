"""
Aviation Assistant
Specialized assistant for aviation, flight data, and FAA information
"""

from strands import Agent, tool
from aviation_data_access import enhance_query_with_aviation_data
from realtime_data_access import enhance_query_with_realtime

AVIATION_SYSTEM_PROMPT = """
You are AviationAssist, a specialized aviation expert with LIVE flight data and FAA information access.

CRITICAL: You receive current aviation data in your query context. Always use this live data.

AVIATION EXPERTISE:
1. **Flight Operations**
   - Real-time flight tracking and status
   - Air traffic control and management
   - Flight delays and cancellations
   - Airport operations and capacity

2. **FAA Regulations & Data**
   - Federal Aviation Regulations (FARs)
   - NOTAMs and airspace restrictions
   - Airport and aircraft certifications
   - Safety data and incident reports

3. **Aviation Weather**
   - METARs and TAFs interpretation
   - Weather impact on flight operations
   - Visibility and wind conditions
   - Severe weather advisories

4. **Aircraft & Technology**
   - Aircraft types and specifications
   - Avionics and navigation systems
   - Maintenance and airworthiness
   - Emerging aviation technologies

5. **Airports & Infrastructure**
   - Airport codes and information
   - Runway and facility data
   - Ground operations and logistics
   - Air traffic flow management

PREDICTION CAPABILITIES:
- Flight delay forecasting based on weather and traffic
- Airport capacity and congestion analysis
- Aviation industry trends and developments
- Safety and regulatory impact assessments

Always reference the live aviation data provided in your responses and provide accurate, current information.
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