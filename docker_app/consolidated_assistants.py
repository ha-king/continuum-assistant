from strands import Agent, tool
from real_time_data import enhance_query_with_realtime

# Consolidated Financial Assistant (combines financial, crypto, economics)
@tool
def financial_assistant(query: str) -> str:
    """Handles finance, cryptocurrency, economics, and tokenomics queries"""
    query = enhance_query_with_realtime(query, "financial")
    
    system_prompt = """
    You are a comprehensive financial expert covering:
    - Traditional finance and accounting
    - Cryptocurrency and blockchain markets
    - Economic analysis and trends
    - Tokenomics and DeFi protocols
    
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
    You are a comprehensive research expert with real-time web access covering:
    - Internet research and information gathering
    - Website analysis and company intelligence
    - Data analysis and predictive modeling
    - Public records and business research
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(query))