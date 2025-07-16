from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from web_browser_assistant import web_browser_assistant

OPENSOURCE_SUPPLY_CHAIN_SYSTEM_PROMPT = """
You are OpenSourceSupplyChainAssist, a specialized open-source software supply chain expert. Your role is to:

1. Supply Chain Security:
   - Dependency management and analysis
   - Vulnerability scanning and remediation
   - Software bill of materials (SBOM)
   - Supply chain attack prevention

2. Open Source Governance:
   - License compliance and management
   - Contributor verification and trust
   - Code review and security practices
   - Maintainer sustainability models

3. Ecosystem Management:
   - Package repository security
   - Distribution and delivery pipelines
   - Community health and governance
   - Risk assessment and mitigation

Provide open-source supply chain expertise with security and governance best practices.
"""

@tool
def opensource_supply_chain_assistant(query: str) -> str:
    """
    Process open-source supply chain queries with expert security guidance.
    
    Args:
        query: An open-source supply chain question or security request
        
    Returns:
        Expert open-source supply chain guidance and security analysis
    """
    try:
        print("Routed to Open Source Supply Chain Assistant")
        enhanced_query = enhance_query_with_realtime(query, "opensource_supply_chain")

        
        formatted_query = f"Provide expert open-source supply chain analysis and guidance for: {enhanced_query}"
        
        # Add web browsing for current data if needed

        
        if any(word in query.lower() for word in ['current', 'latest', 'today', 'recent', 'now']):

        
            try:

        
                web_data = web_browser_assistant(f"Current research data: {query}")

        
                formatted_query += f"\n\nCurrent data from web: {web_data}"

        
            except:

        
                pass

        
        

        
        opensource_agent = Agent(
            system_prompt=OPENSOURCE_SUPPLY_CHAIN_SYSTEM_PROMPT,
            tools=[],
        )
        
        agent_response = opensource_agent(formatted_query)
        text_response = str(agent_response)

        if len(text_response) > 0:
            return text_response
        
        return "Unable to process the open-source supply chain query."
            
    except Exception as e:
        return f"Open-source supply chain analysis error: {str(e)}"