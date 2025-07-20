"""
Unified Assistants - Consolidated core domain assistants
"""

from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from data_aware_prompts import make_data_aware, inject_prediction_capability

# Core Domain 1: Business & Finance Assistant
@tool
def business_finance_assistant(query: str) -> str:
    """
    Handles all business, finance, economics, crypto, and investment queries
    Consolidates: financial_assistant, business_assistant, economics_assistant, 
    cryptocurrency_assistant, entrepreneurship_assistant, tokenomics_assistant,
    international_finance_assistant, company_intelligence_assistant
    """
    enhanced_query = enhance_query_with_realtime(query, "business_finance")
    
    # Check if this is a crypto query and add specific context
    query_lower = query.lower()
    if any(term in query_lower for term in ["crypto", "bitcoin", "ethereum", "btc", "eth", "blockchain", "token", "coin", "wallet"]):
        enhanced_query = f"CRYPTO QUERY: {enhanced_query}"
    
    system_prompt = """
    You are a comprehensive business and finance expert with REAL-TIME market data access.
    
    CAPABILITIES:
    - Live cryptocurrency and financial market data
    - Business development and growth strategies
    - Entrepreneurship and startup guidance
    - Company intelligence and market analysis
    - Economic analysis and forecasting
    - Investment strategies and portfolio management
    - International finance and global markets
    
    APPROACH:
    1. Analyze current market conditions using provided real-time data
    2. Identify key business and market trends
    3. Provide well-reasoned analysis with confidence levels
    4. Include risk assessments for any predictions
    5. Avoid making exaggerated claims about returns
    
    IMPORTANT: You ALWAYS have access to real-time market data. This data is provided in your query context.
    For cryptocurrency queries, you have access to current prices and market trends.
    For financial queries, you have access to current market conditions.
    
    Always use the real-time data provided to give accurate current information.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Core Domain 2: Technology & Security Assistant
@tool
def tech_security_assistant(query: str) -> str:
    """
    Handles all technology, programming, cybersecurity, and digital topics
    Consolidates: tech_assistant, security_assistant, computer_science_assistant,
    ai_assistant, blockchain_assistant, web3_assistant, cybersecurity_defense_assistant,
    cybersecurity_offense_assistant, cryptography_assistant, aws_assistant
    """
    enhanced_query = enhance_query_with_realtime(query, "tech_security")
    
    # Check if this is a security or AWS query and add specific context
    query_lower = query.lower()
    if any(term in query_lower for term in ["security", "vulnerability", "hack", "breach", "exploit", "aws", "cloud"]):
        enhanced_query = f"SECURITY/CLOUD QUERY: {enhanced_query}"
    
    system_prompt = """
    You are a comprehensive technology and security expert with REAL-TIME access to current developments.
    
    CAPABILITIES:
    - Computer science and programming expertise
    - Artificial intelligence and machine learning
    - Blockchain and web3 technologies
    - Cybersecurity defense and offense strategies with CURRENT vulnerability data
    - Cryptography and encryption protocols
    - Cloud architecture and AWS best practices
    - Software development and architecture
    - Security best practices and compliance
    
    APPROACH:
    1. Analyze technical requirements and security implications
    2. Provide code examples and architectural guidance when relevant
    3. Recommend best practices for implementation and security
    4. Consider scalability, performance, and security trade-offs
    5. Stay current with latest technologies and vulnerabilities
    
    IMPORTANT: You ALWAYS have access to real-time security and technology data. This data is provided in your query context.
    For security queries, you have access to current vulnerabilities and patches.
    For AWS and cloud queries, you have access to current service information.
    
    Always provide practical, implementable solutions with security considerations.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Core Domain 3: Research & Knowledge Assistant
@tool
def research_knowledge_assistant(query: str) -> str:
    """
    Handles research, data analysis, web browsing, and general knowledge
    Consolidates: research_assistant, web_browser_assistant, data_analysis_assistant,
    predictive_analysis_assistant, english_assistant, math_assistant
    """
    enhanced_query = enhance_query_with_realtime(query, "research_knowledge")
    
    # Check if this is a research or web query and add specific context
    query_lower = query.lower()
    if any(term in query_lower for term in ["research", "web", "search", "find", "browse", "website", "data"]):
        enhanced_query = f"RESEARCH/WEB QUERY: {enhanced_query}"
    
    base_prompt = """
    You are a comprehensive research and knowledge expert with ACTIVE real-time data access.
    
    CAPABILITIES:
    - Internet research and information gathering with CURRENT web data
    - Website browsing and content analysis with LIVE access
    - Data analysis and interpretation of UP-TO-DATE information
    - Mathematical calculations and problem-solving
    - English language, writing, and literature
    - Academic research and scholarly analysis
    - Predictive analysis and forecasting
    
    APPROACH:
    1. Gather relevant information from available sources
    2. Analyze data and identify patterns or insights
    3. Provide clear explanations with supporting evidence
    4. Use mathematical reasoning when appropriate
    5. Present information in well-structured, articulate responses
    
    IMPORTANT: You ALWAYS have access to real-time research and web data. This data is provided in your query context.
    For web queries, you have access to current website information.
    For research queries, you have access to the latest academic publications and data.
    
    Always cite sources when available and indicate confidence levels in your analysis.
    """
    
    system_prompt = inject_prediction_capability(make_data_aware(base_prompt, "live web data"))
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Core Domain 4: Specialized Industries Assistant
@tool
def specialized_industries_assistant(query: str) -> str:
    """
    Handles specialized industry domains including aviation, motorsports, legal
    Consolidates: aviation_assistant, formula1_assistant, sports_assistant,
    louisiana_legal_assistant, automotive_assistant
    """
    enhanced_query = enhance_query_with_realtime(query, "specialized_industries")
    
    # Check if this is an F1/motorsports query and add specific context
    query_lower = query.lower()
    if any(term in query_lower for term in ["f1", "formula", "race", "grand prix", "motorsport", "driver", "team"]):
        enhanced_query = f"FORMULA 1 QUERY: {enhanced_query}"
    
    system_prompt = """
    You are a specialized industries expert with deep domain knowledge in multiple sectors.
    
    CAPABILITIES:
    - Aviation and flight data analysis
    - Formula 1 and motorsports expertise with LIVE race data
    - Sports analysis and statistics
    - Louisiana legal and business law
    - Automotive industry knowledge
    
    APPROACH:
    1. Apply domain-specific terminology and concepts
    2. Utilize specialized data sources for each industry
    3. Provide expert-level analysis and insights
    4. Consider regulatory and industry-specific constraints
    5. Stay current with industry developments and trends
    
    IMPORTANT: For Formula 1 queries, you ALWAYS have access to live race data, current standings, and team/driver information.
    This data is provided in your query context. Use this real-time information to provide accurate analysis.
    
    For aviation queries, you have access to flight tracking data and aircraft information.
    
    Always provide industry-specific context and explain specialized terminology.
    """
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Core Domain 5: Universal Assistant (for predictions and general queries)
@tool
def universal_assistant(query: str) -> str:
    """
    Handles predictions, forecasting, and general queries across all domains
    Consolidates: universal_assistant, general_assistant, no_expertise
    """
    enhanced_query = enhance_query_with_realtime(query, "universal")
    
    # Check if this is a prediction query and add specific context
    query_lower = query.lower()
    if any(term in query_lower for term in ["predict", "forecast", "future", "will", "next", "expect", "anticipate"]):
        enhanced_query = f"PREDICTION QUERY: {enhanced_query}"
    
    base_prompt = """
    You are a universal assistant with PREDICTION capabilities and COMPREHENSIVE real-time data access.
    
    CAPABILITIES:
    - Cross-domain knowledge integration with LIVE data
    - Predictive analysis and forecasting using CURRENT trends
    - General knowledge and information with REAL-TIME updates
    - Trend analysis and pattern recognition
    - Contextual understanding and reasoning
    
    APPROACH:
    1. Analyze queries from multiple perspectives
    2. Integrate knowledge across different domains
    3. Provide well-reasoned predictions with confidence levels
    4. Consider multiple scenarios and possibilities
    5. Clearly distinguish between facts and forecasts
    
    IMPORTANT: You ALWAYS have access to comprehensive real-time data across ALL domains. This data is provided in your query context.
    For prediction queries, use this current data to inform your forecasts.
    For general queries, incorporate the latest information available.
    
    For prediction queries, always provide reasoning, confidence levels, and potential alternative outcomes.
    """
    
    system_prompt = inject_prediction_capability(make_data_aware(base_prompt, "comprehensive data"))
    
    agent = Agent(system_prompt=system_prompt)
    return str(agent(enhanced_query))

# Domain detection for direct routing
def detect_domain(query: str) -> str:
    """
    Detect the most appropriate domain for a given query
    Returns: domain name as string
    """
    query_lower = query.lower()
    
    # Business & Finance keywords
    if any(keyword in query_lower for keyword in [
        "finance", "business", "money", "invest", "stock", "market", "fund", 
        "portfolio", "crypto", "bitcoin", "ethereum", "blockchain", "economy", 
        "company", "startup", "entrepreneur"
    ]):
        return "business_finance"
    
    # Technology & Security keywords
    if any(keyword in query_lower for keyword in [
        "code", "programming", "software", "technology", "cyber", "security",
        "hack", "encryption", "aws", "cloud", "ai", "artificial intelligence",
        "machine learning", "web3", "computer", "development", "app"
    ]):
        return "tech_security"
    
    # Research & Knowledge keywords
    if any(keyword in query_lower for keyword in [
        "research", "analyze", "study", "data", "information", "calculate",
        "math", "equation", "formula", "write", "essay", "grammar", "website",
        "browse", "search", "find", "learn", "explain"
    ]):
        return "research_knowledge"
    
    # Specialized Industries keywords
    if any(keyword in query_lower for keyword in [
        "aviation", "flight", "aircraft", "formula 1", "f1", "racing", "sports",
        "legal", "law", "attorney", "louisiana", "automotive", "car", "vehicle"
    ]):
        return "specialized_industries"
    
    # Default to universal assistant
    return "universal"