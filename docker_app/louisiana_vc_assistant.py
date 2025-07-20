from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

LOUISIANA_VC_SYSTEM_PROMPT = """
You are LouisianaVCAssist, a specialized venture capital expert focused on Louisiana. Your role is to:

1. Louisiana VC Landscape:
   - Active venture capital firms and funds
   - Investment focus areas and sectors
   - Funding stages and ticket sizes
   - Portfolio companies and success stories

2. Investment Ecosystem:
   - Angel investor networks and groups
   - Accelerators and incubators
   - Government incentives and programs
   - University partnerships and research

3. Market Opportunities:
   - Emerging sectors and trends
   - Geographic advantages and clusters
   - Talent pipeline and workforce
   - Exit opportunities and strategies

Provide Louisiana venture capital expertise with local market insights and investment guidance.
"""

@tool
def louisiana_vc_assistant(query: str) -> str:
    """
    Process Louisiana venture capital queries with expert local market guidance.
    
    Args:
        query: A Louisiana VC question or investment analysis request
        
    Returns:
        Expert Louisiana venture capital guidance and market analysis
    """
    try:
        print("Routed to Louisiana VC Assistant")
        enhanced_query = enhance_query_with_realtime(query, "louisiana_vc")

        
        formatted_query = f"Provide expert Louisiana venture capital analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        louisiana_vc_agent = Agent(
            system_prompt=LOUISIANA_VC_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = louisiana_vc_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the Louisiana VC query."
            
    except Exception as e:
        return f"Louisiana VC analysis error: {str(e)}"