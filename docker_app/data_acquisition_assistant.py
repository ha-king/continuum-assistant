from strands import Agent, tool
from web_browser_assistant import web_browser_assistant

DATA_ACQUISITION_SYSTEM_PROMPT = """
You are DataAcquisitionAssist, a specialized data acquisition expert. Your role is to:

1. Data Collection Methods:
   - Sensor networks and IoT devices
   - Web scraping and API integration
   - Database extraction and ETL processes
   - Real-time streaming data capture

2. Data Quality & Validation:
   - Data validation and cleansing
   - Error detection and correction
   - Sampling strategies and techniques
   - Data integrity and consistency

3. Acquisition Systems:
   - Data pipeline architecture
   - Storage and retrieval systems
   - Scalability and performance optimization
   - Security and compliance considerations

Provide data acquisition expertise with technical implementation and best practices.
"""

@tool
def data_acquisition_assistant(query: str) -> str:
    """
    Process data acquisition queries with expert technical guidance.
    
    Args:
        query: A data acquisition question or implementation request
        
    Returns:
        Expert data acquisition guidance and technical analysis
    """
    try:
        print("Routed to Data Acquisition Assistant")
        
        formatted_query = f"Provide expert data acquisition analysis and guidance for: {query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        data_acq_agent = Agent(
            system_prompt=DATA_ACQUISITION_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = data_acq_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return f"{text_response}\n\n**References Used:** Data acquisition methodologies, sensor technologies, ETL best practices"
        
        return "Unable to process the data acquisition query."
            
    except Exception as e:
        return f"Data acquisition analysis error: {str(e)}"