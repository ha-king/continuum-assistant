from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

ECONOMICS_SYSTEM_PROMPT = """
You are EconomicsAssist, a specialized economics expert. Your role is to:

1. Macroeconomics:
   - Economic indicators and analysis
   - Monetary and fiscal policy
   - International trade and finance
   - Economic cycles and forecasting

2. Microeconomics:
   - Market structures and competition
   - Consumer and producer theory
   - Price mechanisms and elasticity
   - Game theory applications

3. Applied Economics:
   - Behavioral economics
   - Development economics
   - Environmental economics
   - Financial economics and markets

Provide economic analysis with theoretical foundations and practical applications.
"""

@tool
def economics_assistant(query: str) -> str:
    """
    Process economics-related queries with expert economic analysis.
    
    Args:
        query: An economics question or analysis request
        
    Returns:
        Expert economic guidance and analysis
    """
    try:
        print("Routed to Economics Assistant")
        
        formatted_query = f"Provide expert economic analysis and guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        economics_agent = Agent(
            system_prompt=ECONOMICS_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = economics_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the economics query."
            
    except Exception as e:
        return f"Economics analysis error: {str(e)}"