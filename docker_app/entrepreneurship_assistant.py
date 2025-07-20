from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

ENTREPRENEURSHIP_SYSTEM_PROMPT = """
You are EntrepreneurshipAssist, a specialized entrepreneurship success expert. Your role is to:

1. Startup Strategy:
   - Business model development
   - Market validation and research
   - Competitive analysis and positioning
   - Go-to-market strategies

2. Business Operations:
   - Team building and leadership
   - Product development and iteration
   - Sales and marketing execution
   - Financial planning and fundraising

3. Growth & Scaling:
   - Scaling operations and systems
   - Partnership and alliance strategies
   - Exit strategies and acquisitions
   - Innovation and disruption tactics

Provide entrepreneurship guidance with actionable strategies and real-world implementation insights.
"""

@tool
def entrepreneurship_assistant(query: str) -> str:
    """
    Process entrepreneurship queries with expert business success guidance.
    
    Args:
        query: An entrepreneurship question or business strategy request
        
    Returns:
        Expert entrepreneurship guidance and strategic analysis
    """
    try:
        print("Routed to Entrepreneurship Assistant")
        enhanced_query = enhance_query_with_realtime(query, "entrepreneurship")

        
        formatted_query = f"Provide expert entrepreneurship analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        entrepreneur_agent = Agent(
            system_prompt=ENTREPRENEURSHIP_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = entrepreneur_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the entrepreneurship query."
            
    except Exception as e:
        return f"Entrepreneurship analysis error: {str(e)}"