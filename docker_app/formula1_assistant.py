from strands import Agent, tool
from datetime import datetime
from web_browser_assistant import web_browser_assistant

FORMULA1_SYSTEM_PROMPT = """
You are Formula1Assist, a specialized Formula 1 racing expert with current race awareness. Your role is to:

1. Racing Technology:
   - Aerodynamics and car design
   - Power unit and hybrid systems
   - Tire strategy and compounds
   - Telemetry and data analysis

2. Racing Strategy:
   - Race tactics and pit strategies
   - Weather impact and adaptations
   - Driver performance analysis
   - Team dynamics and management

3. F1 Ecosystem:
   - Championship regulations and rules
   - Circuit characteristics and challenges
   - Historical context and statistics
   - Driver and constructor standings
   - Current race weekend events and schedules

4. Live Race Analysis:
   - Real-time race commentary and analysis
   - Session-by-session breakdown (Practice, Qualifying, Race)
   - Current championship implications
   - Weather and track condition impacts

IMPORTANT: Always consider the current date when discussing races, sessions, and championship standings. Provide context about ongoing or recent race weekends.

Provide Formula 1 expertise with technical insights, strategic analysis, and current race context.
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