from strands import Agent, tool
from datetime import datetime
import requests

def get_crypto_data(symbol):
    """Get crypto data from multiple sources"""
    import requests
    
    # Try Coinbase first (free, no auth needed)
    coinbase_map = {
        'bitcoin': 'BTC-USD', 'btc': 'BTC-USD',
        'ethereum': 'ETH-USD', 'eth': 'ETH-USD',
        'apecoin': 'APE-USD', 'ape': 'APE-USD',
        'dogecoin': 'DOGE-USD', 'doge': 'DOGE-USD',
        'cardano': 'ADA-USD', 'ada': 'ADA-USD',
        'solana': 'SOL-USD', 'sol': 'SOL-USD'
    }
    
    pair = coinbase_map.get(symbol.lower())
    if pair:
        try:
            response = requests.get(f'https://api.coinbase.com/v2/exchange-rates?currency={pair.split("-")[0]}', timeout=5)
            if response.status_code == 200:
                data = response.json().get('data', {}).get('rates', {})
                price = data.get('USD')
                if price:
                    return f"${float(price):.4f} (Coinbase)"
        except: pass
    
    # Fallback to CoinGecko
    gecko_map = {
        'bitcoin': 'bitcoin', 'btc': 'bitcoin',
        'ethereum': 'ethereum', 'eth': 'ethereum', 
        'apecoin': 'apecoin', 'ape': 'apecoin',
        'dogecoin': 'dogecoin', 'doge': 'dogecoin',
        'cardano': 'cardano', 'ada': 'cardano',
        'solana': 'solana', 'sol': 'solana'
    }
    
    coin_id = gecko_map.get(symbol.lower())
    if coin_id:
        try:
            response = requests.get(f'https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true', timeout=5)
            if response.status_code == 200:
                data = response.json().get(coin_id, {})
                if data:
                    return f"${data.get('usd', 'N/A')} (24h: {data.get('usd_24h_change', 0):.2f}%)"
        except: pass
    
    return None

def get_f1_data():
    """Get current F1 race data from multiple sources"""
    try:
        # Try ESPN F1 schedule
        response = requests.get('https://www.espn.com/f1/schedule', timeout=5)
        if response.status_code == 200:
            import re
            content = response.text
            # Extract race info from ESPN page
            race_match = re.search(r'<h3[^>]*>([^<]+)</h3>.*?<span[^>]*>([^<]+)</span>', content, re.DOTALL)
            if race_match:
                return f"Next F1 Race: {race_match.group(1)} - {race_match.group(2)} (ESPN)"
    except: pass
    
    try:
        # Try Ergast API
        response = requests.get('https://ergast.com/api/f1/current/next.json', timeout=5)
        if response.status_code == 200:
            data = response.json()
            races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
            if races:
                race = races[0]
                return f"Next F1 Race: {race.get('raceName', 'Unknown')} at {race.get('Circuit', {}).get('circuitName', 'Unknown')} on {race.get('date', 'TBD')} (Ergast)"
    except: pass
    
    current_date = datetime.now()
    return f"Current F1 season: {current_date.year} - Sources: ESPN F1, OpenF1 GitHub, Formula1.com"

def enhance_query_with_realtime(query, assistant_type):
    """Add current datetime and real-time data to queries"""
    current_datetime = datetime.now().strftime("%A, %B %d, %Y at %I:%M %p UTC")
    context = f"CURRENT DATE/TIME: {current_datetime}\n\nLIVE DATA:\n"
    
    # Get real-time data for relevant queries
    if any(word in query.lower() for word in ['current', 'latest', 'today', 'now', 'price', 'race', 'f1', 'formula']):
        # F1 data for racing queries
        if any(word in query.lower() for word in ['f1', 'formula', 'race', 'grand prix']):
            f1_data = get_f1_data()
            if f1_data:
                context += f"F1 DATA: {f1_data}\n"
        
        # Extract crypto symbols from query
        words = query.lower().split()
        for word in words:
            crypto_data = get_crypto_data(word)
            if crypto_data:
                context += f"LIVE {word.upper()} DATA: {crypto_data}\n"
        
        # Get web data for other current queries
        try:
            from web_browser_assistant import web_browser_assistant
            web_data = web_browser_assistant(f"Current {assistant_type} data: {query}")
            if web_data and len(web_data) > 50:
                context += f"Real-time data: {web_data[:200]}...\n"
        except: pass
    
    return f"{context}\nQuery: {query}"

# Consolidated Financial Assistant (combines financial, crypto, economics)
@tool
def financial_assistant(query: str) -> str:
    """Handles finance, cryptocurrency, economics, and tokenomics queries"""
    query = enhance_query_with_realtime(query, "financial")
    
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

# Consolidated Sports Assistant (includes F1, motorsports)
@tool
def sports_assistant(query: str) -> str:
    """Handles Formula 1, motorsports, and sports analysis with real-time data"""
    query = enhance_query_with_realtime(query, "sports")
    
    system_prompt = f"""
    You are a comprehensive sports expert with REAL-TIME data access covering:
    - Formula 1 racing with current race schedules and results
    - Motorsports analysis and technical insights
    - Live race data and championship standings
    - Current sports events and schedules
    
    IMPORTANT: You receive live data including current date/time and F1 race information.
    Always use the real-time data provided to give accurate current information.
    
    Current context: It is currently {datetime.now().strftime("%B %Y")}. 
    Always check the live data provided for the most current race information.
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