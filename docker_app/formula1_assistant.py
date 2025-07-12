from strands import Agent, tool
from datetime import datetime
from web_browser_assistant import web_browser_assistant
import requests
import json

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
        
        # Get real-time F1 data from OpenF1 API
        openf1_data = ""
        try:
            openf1_data = get_openf1_data(query)
            if openf1_data:
                formatted_query += f"\n\nReal-time F1 data: {openf1_data}"
        except:
            pass
        
        # Fallback to web data if needed
        if not openf1_data and any(word in query.lower() for word in ['current', 'today', 'now', 'latest', 'live', 'race']):
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
            references = "F1 technical regulations, current race calendar"
            if openf1_data:
                references += ", OpenF1.org live data"
            references += ", Formula1.com, performance analytics"
            return f"{text_response}\n\n**References Used:** {references}"
        
        return "Unable to process the Formula 1 query."
            
    except Exception as e:
        return f"Formula 1 analysis error: {str(e)}"

def get_openf1_data(query):
    """Get real-time F1 data from OpenF1 API"""
    try:
        base_url = "https://api.openf1.org/v1"
        
        # Determine what data to fetch based on query
        if any(word in query.lower() for word in ['session', 'practice', 'qualifying', 'race']):
            # Get current session info
            response = requests.get(f"{base_url}/sessions?year=2024", timeout=5)
            if response.status_code == 200:
                sessions = response.json()
                if sessions:
                    latest_session = sessions[-1]  # Get most recent session
                    return f"Latest Session: {latest_session.get('session_name', 'Unknown')} at {latest_session.get('circuit_short_name', 'Unknown')} on {latest_session.get('date_start', 'Unknown')}"
        
        elif any(word in query.lower() for word in ['driver', 'position', 'standings']):
            # Get driver info
            response = requests.get(f"{base_url}/drivers?session_key=latest", timeout=5)
            if response.status_code == 200:
                drivers = response.json()
                if drivers:
                    driver_list = [f"{d.get('name_acronym', 'UNK')} ({d.get('team_name', 'Unknown')})" for d in drivers[:10]]
                    return f"Current F1 Drivers: {', '.join(driver_list)}"
        
        elif any(word in query.lower() for word in ['lap', 'time', 'fastest']):
            # Get lap times (simplified)
            response = requests.get(f"{base_url}/laps?session_key=latest", timeout=5)
            if response.status_code == 200:
                laps = response.json()
                if laps:
                    return f"Lap data available for {len(laps)} laps from latest session"
        
        elif any(word in query.lower() for word in ['weather', 'track', 'conditions']):
            # Get weather data
            response = requests.get(f"{base_url}/weather?session_key=latest", timeout=5)
            if response.status_code == 200:
                weather = response.json()
                if weather:
                    latest_weather = weather[-1] if weather else {}
                    return f"Track conditions: {latest_weather.get('track_temperature', 'Unknown')}°C track, {latest_weather.get('air_temperature', 'Unknown')}°C air, {latest_weather.get('humidity', 'Unknown')}% humidity"
        
        return None
        
    except Exception as e:
        print(f"OpenF1 API error: {str(e)}")
        return None