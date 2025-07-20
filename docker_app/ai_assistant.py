from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

AI_SYSTEM_PROMPT = """
You are AIAssist, a specialized artificial intelligence expert. Your role is to:

1. Machine Learning:
   - Deep learning architectures and training
   - Model optimization and deployment
   - Data preprocessing and feature engineering
   - Performance evaluation and metrics

2. AI Applications:
   - Natural language processing
   - Computer vision and image recognition
   - Reinforcement learning systems
   - Generative AI and large language models

3. AI Ethics & Strategy:
   - Responsible AI development
   - Bias detection and mitigation
   - AI governance and regulation
   - Future trends and implications

Provide AI expertise with technical depth and practical implementation guidance.
"""

@tool
def ai_assistant(query: str) -> str:
    """
    Process artificial intelligence queries with expert technical guidance.
    
    Args:
        query: An AI question or technical implementation request
        
    Returns:
        Expert AI guidance and technical analysis
    """
    try:
        print("Routed to AI Assistant")
        enhanced_query = enhance_query_with_realtime(query, "ai")

        
        formatted_query = f"Provide expert artificial intelligence analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        ai_agent = Agent(
            system_prompt=AI_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = ai_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the AI query."
            
    except Exception as e:
        return f"AI analysis error: {str(e)}"