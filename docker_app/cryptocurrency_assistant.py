from strands import Agent, tool
from realtime_data_access import enhance_query_with_realtime
from crypto_data_service import get_enhanced_crypto_data
from crypto_prediction_engine import get_crypto_prediction
from web_browser_assistant import web_browser_assistant
from crypto_performance_monitor import performance_tracking
from coinbase_api_service import coinbase_service
from datetime import datetime

CRYPTOCURRENCY_SYSTEM_PROMPT = """
You are CryptocurrencyAssist, a specialized cryptocurrency expert with real-time market data access. Your role is to:

1. Cryptocurrency Markets:
   - Real-time market analysis and trends
   - Trading strategies and risk management
   - Technical and fundamental analysis
   - Market psychology and sentiment analysis

2. Digital Assets:
   - Bitcoin, Ethereum, and altcoins
   - Stablecoins and CBDCs
   - NFTs and digital collectibles
   - Asset valuation methods and tokenomics

3. Investment & Trading:
   - Portfolio management strategies
   - DeFi protocols and yield farming
   - Regulatory compliance considerations
   - Security and custody solutions

4. Technical Analysis:
   - Chart patterns and indicators
   - Support/resistance levels
   - Moving averages and oscillators
   - Volume analysis and market depth

5. On-Chain Analysis:
   - Blockchain metrics and network health
   - Wallet activity and whale movements
   - Smart contract interactions
   - Layer 2 and scaling solutions

Always include:
- Current price data when discussing specific cryptocurrencies
- Timestamp for when analysis was generated
- Risk disclaimers for investment advice
- Educational context for technical concepts

You have access to real-time cryptocurrency price data and market metrics.
"""

@tool
@performance_tracking
def cryptocurrency_assistant(query: str) -> str:
    """
    Process cryptocurrency-related queries with expert market analysis and real-time data.
    
    Args:
        query: A cryptocurrency question or market analysis request
        
    Returns:
        Expert cryptocurrency guidance and market analysis with current data
    """
    try:
        print("Routed to Cryptocurrency Assistant")
        
        # Get enhanced crypto-specific data with Coinbase integration
        crypto_data = get_enhanced_crypto_data(query)
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        
        # Add historical data context for trend analysis
        historical_context = ""
        if any(word in query.lower() for word in ['historical', 'trend', 'performance', 'chart', 'week', 'month']):
            try:
                # Extract crypto symbols from query
                symbols = []
                crypto_keywords = {'bitcoin': 'BTC', 'btc': 'BTC', 'ethereum': 'ETH', 'eth': 'ETH', 'solana': 'SOL', 'sol': 'SOL'}
                for keyword, symbol in crypto_keywords.items():
                    if keyword in query.lower():
                        symbols.append(symbol)
                
                if not symbols:
                    symbols = ['BTC']  # Default to Bitcoin
                
                for symbol in symbols[:2]:  # Limit to 2 symbols for performance
                    days = 7
                    if 'month' in query.lower():
                        days = 30
                    elif 'week' in query.lower():
                        days = 7
                    
                    historical_data = coinbase_service.get_historical_prices(f"{symbol}-USD", days)
                    if historical_data and len(historical_data) >= 2:
                        start_price = historical_data[0]['price']
                        end_price = historical_data[-1]['price']
                        change = ((end_price - start_price) / start_price) * 100
                        historical_context += f"{symbol} {days}d trend: {change:+.2f}% (${start_price:,.2f} → ${end_price:,.2f})\n"
            except Exception as e:
                print(f"Historical data error: {str(e)}")
        
        # Add real-time context
        context = f"CURRENT TIME: {current_time}\n\nCRYPTO MARKET DATA: {crypto_data}\n\n"
        if historical_context:
            context += f"HISTORICAL ANALYSIS:\n{historical_context}\n"
        
        # Add prediction data for forecasting queries
        if any(word in query.lower() for word in ['predict', 'forecast', 'potential', 'growth', 'future', '10x', 'price target']):
            prediction_data = get_crypto_prediction(query)
            if prediction_data:
                context += f"PREDICTION DATA:\n{prediction_data}\n\n"
        
        # Add general real-time context
        enhanced_query = enhance_query_with_realtime(query, "crypto")
        
        # For price comparison queries, add multi-symbol analysis
        if any(word in query.lower() for word in ['compare', 'vs', 'versus', 'better', 'which']):
            try:
                # Extract multiple symbols for comparison
                symbols = []
                crypto_keywords = {
                    'bitcoin': 'BTC', 'btc': 'BTC', 'ethereum': 'ETH', 'eth': 'ETH',
                    'solana': 'SOL', 'sol': 'SOL', 'cardano': 'ADA', 'ada': 'ADA',
                    'polkadot': 'DOT', 'dot': 'DOT'
                }
                for keyword, symbol in crypto_keywords.items():
                    if keyword in query.lower() and symbol not in symbols:
                        symbols.append(symbol)
                
                if len(symbols) >= 2:
                    comparison_data = coinbase_service.get_market_data(symbols)
                    if comparison_data and 'prices' in comparison_data:
                        context += "PRICE COMPARISON:\n"
                        for symbol, price_info in comparison_data['prices'].items():
                            context += f"{symbol}: ${price_info['price']:,.2f}\n"
                        context += "\n"
            except Exception as e:
                print(f"Comparison data error: {str(e)}")
        
        # For queries about very recent events or news, add web browsing results
        if any(word in query.lower() for word in ['latest', 'news', 'today', 'recent', 'announcement', 'launch']):
            try:
                web_results = web_browser_assistant(f"latest cryptocurrency news {query}")
                if web_results and len(web_results) > 20:
                    context += f"RECENT NEWS: {web_results[:500]}...\n\n"
            except Exception as web_error:
                print(f"Web browsing error: {str(web_error)}")
        
        # Format query with all context
        formatted_query = f"{context}User query: {query}\n\nProvide expert cryptocurrency analysis with current market data."
        
        # Create agent with enhanced system prompt
        crypto_agent = Agent(
            system_prompt=CRYPTOCURRENCY_SYSTEM_PROMPT,
            tools=[],
        )
        
        # Get response
        agent_response = crypto_agent(formatted_query)
        text_response = str(agent_response)

        # Ensure response includes timestamp and data source info
        if len(text_response) > 0:
            if "Analysis timestamp:" not in text_response:
                text_response += f"\n\nAnalysis timestamp: {current_time}"
            if "Data sources:" not in text_response:
                text_response += f"\nData sources: Coinbase API, CoinGecko, Real-time market feeds"
            return text_response
        
        return f"Unable to process the cryptocurrency query. Please try again.\n\nTimestamp: {current_time}"
            
    except Exception as e:
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
        return f"Cryptocurrency analysis error: {str(e)}\n\nTimestamp: {current_time}"