from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime, get_current_datetime
from data_aware_prompts import make_data_aware, inject_prediction_capability
from datetime import datetime
import requests

# Legacy functions removed - now using centralized realtime_data_access module

# Consolidated Financial Assistant (combines financial, crypto, economics)
@tool
def financial_assistant(query: str) -> str:
    """Handles finance, cryptocurrency, economics, and tokenomics queries with real-time data"""
    enhanced_query = enhance_query_with_realtime(query, "financial")
    
    system_prompt = """
    You are a comprehensive financial expert with REAL-TIME market data access.
    
    IMPORTANT: You receive live market data in your query context. Use this data to provide current prices, analysis, and forecasts.
    
    Capabilities:
    - Live cryptocurrency prices and market data
    - Current financial market information  
    - Real-time economic analysis
    - Up-to-date market trends
    
    Always use the real-time data provided to give accurate current information.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Consolidated Security Assistant (combines cybersecurity offense/defense, cryptography)
@tool
def security_assistant(query: str) -> str:
    """Handles cybersecurity, cryptography, and security analysis with real-time threat data"""
    enhanced_query = enhance_query_with_realtime(query, "security")
    
    system_prompt = """
    You are a comprehensive security expert with access to current threat intelligence covering:
    - Cybersecurity defense and offense strategies
    - Cryptography and encryption protocols
    - Security best practices and compliance
    - Threat analysis and risk assessment
    - Current security vulnerabilities and patches
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Consolidated Business Assistant (combines business dev, entrepreneurship, networking)
@tool
def business_assistant(query: str) -> str:
    """Handles business development, entrepreneurship, and professional networking with real-time market data"""
    enhanced_query = enhance_query_with_realtime(query, "business")
    
    system_prompt = """
    You are a comprehensive business expert with access to current market intelligence covering:
    - Business development and growth strategies
    - Entrepreneurship and startup guidance
    - Professional networking and partnerships
    - Company intelligence and market analysis
    - Current business trends and opportunities
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Consolidated Tech Assistant (combines CS, AI, blockchain, web3)
@tool
def tech_assistant(query: str) -> str:
    """Handles computer science, AI, blockchain, and web3 technologies with real-time tech updates"""
    enhanced_query = enhance_query_with_realtime(query, "tech")
    
    system_prompt = """
    You are a comprehensive technology expert with access to current tech developments covering:
    - Computer science and programming
    - Artificial intelligence and machine learning
    - Blockchain and web3 technologies
    - Software architecture and best practices
    - Latest technology trends and innovations
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Consolidated Sports Assistant (includes F1, motorsports)
@tool
def sports_assistant(query: str) -> str:
    """Handles Formula 1, motorsports, and sports analysis with real-time data"""
    enhanced_query = enhance_query_with_realtime(query, "sports")
    
    base_prompt = "You are a comprehensive sports expert covering F1 racing, motorsports analysis, and championship standings."
    system_prompt = inject_prediction_capability(make_data_aware(base_prompt, "live F1"))
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Consolidated Research Assistant (combines research, web browser, data analysis)
@tool
def research_assistant(query: str) -> str:
    """Handles research, web browsing, and data analysis with real-time internet access"""
    enhanced_query = enhance_query_with_realtime(query, "research")
    
    base_prompt = "You are a comprehensive research expert with ACTIVE real-time data access for internet research, website analysis, and current information gathering."
    system_prompt = inject_prediction_capability(make_data_aware(base_prompt, "live web data"))
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))