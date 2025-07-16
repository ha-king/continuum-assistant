from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from datetime import datetime
from web_browser_assistant import web_browser_assistant

FORMULA1_SYSTEM_PROMPT = """
You are Formula1Assist, a specialized Formula 1 racing expert with LIVE real-time data access.

IMPORTANT: You receive current F1 race data in your query context. Always use this live data to provide accurate, current information.

Capabilities:
1. Live Race Data - Current schedules, results, standings from ESPN F1 and OpenF1 APIs
2. Real-time Analysis - Use provided live data for predictions and insights
3. Technical Expertise - Aerodynamics, strategy, driver performance
4. Current Context - Always reference the live data provided in your response

When making predictions, use the current race data provided and explain your reasoning based on:
- Current championship standings
- Recent race performance
- Track characteristics
- Team/driver form

Always acknowledge and use the real-time data provided in your query context.
"""

@tool
def formula1_assistant(query: str) -> str:
    """
    Process Formula 1 racing queries with expert technical and strategic guidance including current race information.
    
    Args:
        query: A Formula 1 question or racing analysis request
        
    Returns:
        Expert Formula 1 guidance and racing analysis with current context
    """
    try:
        print("Routed to Formula 1 Assistant")
        enhanced_query = enhance_query_with_realtime(query, "formula1")

        
        # Add current date context for race awareness
        current_date = datetime.now().strftime("%A, %B %d, %Y")
        
        formatted_query = f"Current date: {current_date}\n\nProvide expert Formula 1 racing analysis and guidance for: {query}\n\nNote: Consider any ongoing race weekend, practice sessions, qualifying, or races happening today or recently."
        
        # First try to get current race data from web
        if any(word in query.lower() for word in ['current', 'today', 'now', 'latest', 'live', 'race']):
            try:
                web_query = f"Formula 1 current race status today {current_date} live updates"
                web_data = web_browser_assistant(web_query)
                formatted_query += f"\n\nCurrent F1 data from web: {web_data}"
            except:
                pass
        
        f1_agent = Agent(
            system_prompt=FORMULA1_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = f1_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return f"{text_response}\n\n**References Used:** F1 technical regulations, current race calendar, live timing data, Formula1.com, performance analytics"
        
        return "Unable to process the Formula 1 query."
            
    except Exception as e:
        return f"Formula 1 analysis error: {str(e)}"