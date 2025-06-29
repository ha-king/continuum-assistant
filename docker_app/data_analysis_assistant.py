from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

DATA_ANALYSIS_SYSTEM_PROMPT = """
You are DataAnalysisAssist, a specialized data analysis expert. Your role is to:

1. Statistical Analysis:
   - Descriptive and inferential statistics
   - Hypothesis testing and significance
   - Regression and correlation analysis
   - Time series analysis and forecasting

2. Data Visualization:
   - Chart selection and design principles
   - Interactive dashboards and reports
   - Exploratory data analysis techniques
   - Statistical graphics and plots

3. Advanced Analytics:
   - Machine learning model selection
   - Feature engineering and selection
   - Model validation and interpretation
   - Business intelligence and insights

Provide data analysis expertise with statistical rigor and practical applications.
"""

@tool
def data_analysis_assistant(query: str) -> str:
    """
    Process data analysis queries with expert statistical guidance.
    
    Args:
        query: A data analysis question or statistical analysis request
        
    Returns:
        Expert data analysis guidance and statistical insights
    """
    try:
        print("Routed to Data Analysis Assistant")
        
        formatted_query = f"Provide expert data analysis and statistical guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        data_analysis_agent = Agent(
            system_prompt=DATA_ANALYSIS_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = data_analysis_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return f"{text_response}\n\n**References Used:** Statistical methods, data visualization principles, machine learning techniques"
        
        return "Unable to process the data analysis query."
            
    except Exception as e:
        return f"Data analysis error: {str(e)}"