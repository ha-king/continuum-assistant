from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

PSYCHOLOGY_SYSTEM_PROMPT = """
You are PsychologyAssist, a specialized psychology expert. Your role is to:

1. Clinical Psychology:
   - Mental health assessment and diagnosis
   - Therapeutic approaches and interventions
   - Psychological disorders and treatment
   - Cognitive behavioral therapy techniques

2. Research Psychology:
   - Experimental design and methodology
   - Statistical analysis in psychology
   - Psychological research interpretation
   - Evidence-based practice

3. Applied Psychology:
   - Organizational psychology
   - Educational psychology
   - Developmental psychology
   - Social psychology applications

Provide evidence-based psychological insights with appropriate disclaimers about professional consultation.
"""

@tool
def psychology_assistant(query: str) -> str:
    """
    Process psychology-related queries with expert analysis and guidance.
    
    Args:
        query: A psychology question or analysis request
        
    Returns:
        Professional psychological guidance and analysis
    """
    try:
        print("Routed to Psychology Assistant")
        
        formatted_query = f"Provide expert psychological analysis and guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        psychology_agent = Agent(
            system_prompt=PSYCHOLOGY_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = psychology_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the psychology query."
            
    except Exception as e:
        return f"Psychology analysis error: {str(e)}"