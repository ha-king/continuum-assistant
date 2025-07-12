from strands import Agent, tool
from datetime import datetime
import requests

def enhance_query_with_realtime(query, assistant_type):
    """Add current datetime and real-time data to queries"""
    current_time = datetime.now().strftime('%A, %B %d, %Y at %I:%M %p UTC')
    context = f"Current date and time: {current_time}\n"
    
    # Add real-time web data for current queries
    if any(word in query.lower() for word in ['current', 'latest', 'today', 'now', 'price']):
        try:
            from web_browser_assistant import web_browser_assistant
            web_data = web_browser_assistant(f"Current {assistant_type} data: {query}")
            if web_data and len(web_data) > 50:
                context += f"Real-time data: {web_data[:200]}...\n"
        except:
            pass
    
    return f"{context}\nQuery: {query}"

# Consolidated Financial Assistant (combines financial, crypto, economics)
@tool
def financial_assistant(query: str) -> str:
    """Handles finance, cryptocurrency, economics, and tokenomics queries"""
    query = enhance_query_with_realtime(query, "financial")
    
    system_prompt = """
    You are a comprehensive financial expert with REAL-TIME market data access covering:
    - Traditional finance and accounting with current market data
    - Cryptocurrency and blockchain markets with live prices
    - Economic analysis and current trends
    - Tokenomics and DeFi protocols with real-time metrics
    
    IMPORTANT: You receive current date/time context. Use this for all analysis.
    Provide expert analysis with real-time data and appropriate risk disclaimers.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))

# Consolidated Security Assistant (combines cybersecurity offense/defense, cryptography)
@tool
def security_assistant(query: str) -> str:
    """Handles cybersecurity, cryptography, and security analysis"""
    query = enhance_query_with_realtime(query, "security")
    
    system_prompt = """
    You are a comprehensive security expert covering:
    - Cybersecurity defense and offense strategies
    - Cryptography and encryption protocols
    - Security best practices and compliance
    - Threat analysis and risk assessment
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))

# Consolidated Business Assistant (combines business dev, entrepreneurship, networking)
@tool
def business_assistant(query: str) -> str:
    """Handles business development, entrepreneurship, and professional networking"""
    query = enhance_query_with_realtime(query, "business")
    
    system_prompt = """
    You are a comprehensive business expert covering:
    - Business development and growth strategies
    - Entrepreneurship and startup guidance
    - Professional networking and partnerships
    - Company intelligence and market analysis
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))

# Consolidated Tech Assistant (combines CS, AI, blockchain, web3)
@tool
def tech_assistant(query: str) -> str:
    """Handles computer science, AI, blockchain, and web3 technologies"""
    query = enhance_query_with_realtime(query, "tech")
    
    system_prompt = """
    You are a comprehensive technology expert covering:
    - Computer science and programming
    - Artificial intelligence and machine learning
    - Blockchain and web3 technologies
    - Software architecture and best practices
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))

# Consolidated Research Assistant (combines research, web browser, data analysis)
@tool
def research_assistant(query: str) -> str:
    """Handles research, web browsing, and data analysis"""
    query = enhance_query_with_realtime(query, "research")
    
    system_prompt = """
    You are a comprehensive research expert with ACTIVE real-time web access covering:
    - Live internet research and current information gathering
    - Real-time website analysis and company intelligence
    - Current data analysis and predictive modeling
    - Live public records and business research
    
    IMPORTANT: You have access to current web data and real-time information.
    Always provide the most current and up-to-date information available.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))