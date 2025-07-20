"""
Crypto Prediction Engine - Enhanced forecasting capabilities for cryptocurrency assistant
"""

import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from direct_crypto_api import get_realtime_price
from crypto_data_service import crypto_data_service

class CryptoPredictionEngine:
    """Engine for cryptocurrency trend analysis and forecasting"""
    
    def __init__(self):
        # Prediction confidence levels
        self.CONFIDENCE_LOW = "low"
        self.CONFIDENCE_MEDIUM = "medium"
        self.CONFIDENCE_HIGH = "high"
        
        # Market sentiment indicators
        self.SENTIMENT_BEARISH = "bearish"
        self.SENTIMENT_NEUTRAL = "neutral"
        self.SENTIMENT_BULLISH = "bullish"
        
        # Time horizons
        self.HORIZON_SHORT = "short-term"  # Days to weeks
        self.HORIZON_MEDIUM = "medium-term"  # Weeks to months
        self.HORIZON_LONG = "long-term"  # Months+
    
    def analyze_growth_potential(self, symbol: str, time_horizon: str) -> Dict[str, Any]:
        """
        Analyze growth potential for a specific cryptocurrency
        
        Args:
            symbol: Cryptocurrency symbol (e.g., BTC)
            time_horizon: Time horizon for analysis (short/medium/long-term)
            
        Returns:
            Dictionary with growth analysis
        """
        # Get current price data directly from API
        price_data = get_realtime_price(symbol)
        if not price_data:
            # Fall back to crypto_data_service if direct API fails
            price_data = crypto_data_service.get_crypto_price(symbol)
            if not price_data:
                return {
                    "symbol": symbol,
                    "error": "Unable to retrieve price data",
                    "timestamp": datetime.now().isoformat()
                }
        
        # Get market overview for context
        market_data = crypto_data_service.get_market_overview()
        
        # Determine base metrics
        current_price = price_data.get("price_usd", 0)
        change_24h = price_data.get("change_24h", 0)
        market_cap = price_data.get("market_cap", 0)
        
        # Default values
        growth_potential = 0
        confidence = self.CONFIDENCE_LOW
        sentiment = self.SENTIMENT_NEUTRAL
        factors = []
        
        # Basic sentiment analysis based on 24h change
        if change_24h > 5:
            sentiment = self.SENTIMENT_BULLISH
            factors.append(f"Strong 24h performance: {change_24h:.2f}%")
        elif change_24h > 2:
            sentiment = self.SENTIMENT_BULLISH
            factors.append(f"Positive 24h performance: {change_24h:.2f}%")
        elif change_24h < -5:
            sentiment = self.SENTIMENT_BEARISH
            factors.append(f"Weak 24h performance: {change_24h:.2f}%")
        elif change_24h < -2:
            sentiment = self.SENTIMENT_BEARISH
            factors.append(f"Negative 24h performance: {change_24h:.2f}%")
        else:
            sentiment = self.SENTIMENT_NEUTRAL
            factors.append(f"Neutral 24h performance: {change_24h:.2f}%")
        
        # Adjust for market cap (smaller cap = higher growth potential but lower confidence)
        if market_cap:
            if market_cap > 100_000_000_000:  # $100B+
                confidence = self.CONFIDENCE_HIGH
                factors.append("Large market cap suggests stability")
                # Large caps have lower growth multiples
                if time_horizon == self.HORIZON_SHORT:
                    growth_potential = 0.2  # 20% potential
                elif time_horizon == self.HORIZON_MEDIUM:
                    growth_potential = 0.5  # 50% potential
                else:
                    growth_potential = 1.0  # 100% potential (2x)
            elif market_cap > 10_000_000_000:  # $10B+
                confidence = self.CONFIDENCE_MEDIUM
                factors.append("Medium market cap suggests moderate growth potential")
                if time_horizon == self.HORIZON_SHORT:
                    growth_potential = 0.3  # 30% potential
                elif time_horizon == self.HORIZON_MEDIUM:
                    growth_potential = 1.0  # 100% potential (2x)
                else:
                    growth_potential = 3.0  # 300% potential (4x)
            else:
                confidence = self.CONFIDENCE_LOW
                factors.append("Smaller market cap suggests higher volatility and growth potential")
                if time_horizon == self.HORIZON_SHORT:
                    growth_potential = 0.5  # 50% potential
                elif time_horizon == self.HORIZON_MEDIUM:
                    growth_potential = 2.0  # 200% potential (3x)
                else:
                    growth_potential = 9.0  # 900% potential (10x)
        
        # Adjust for market sentiment
        if sentiment == self.SENTIMENT_BULLISH:
            growth_potential *= 1.2
            factors.append("Bullish sentiment increases growth potential")
        elif sentiment == self.SENTIMENT_BEARISH:
            growth_potential *= 0.8
            factors.append("Bearish sentiment decreases growth potential")
        
        # Adjust for overall market conditions
        if market_data and "btc_dominance" in market_data:
            btc_dominance = market_data.get("btc_dominance", 50)
            if symbol.upper() == "BTC":
                if btc_dominance > 50:
                    growth_potential *= 1.1
                    factors.append(f"High BTC dominance ({btc_dominance:.1f}%) favorable for Bitcoin")
                else:
                    growth_potential *= 0.9
                    factors.append(f"Lower BTC dominance ({btc_dominance:.1f}%) may limit Bitcoin growth")
            else:
                # For altcoins, lower BTC dominance is better
                if btc_dominance < 40:
                    growth_potential *= 1.2
                    factors.append(f"Low BTC dominance ({btc_dominance:.1f}%) favorable for altcoins")
                elif btc_dominance > 55:
                    growth_potential *= 0.8
                    factors.append(f"High BTC dominance ({btc_dominance:.1f}%) may limit altcoin growth")
        
        # Calculate potential price targets
        potential_price = current_price * (1 + growth_potential)
        
        return {
            "symbol": symbol,
            "current_price": current_price,
            "time_horizon": time_horizon,
            "growth_potential": growth_potential,
            "potential_multiple": 1 + growth_potential,
            "potential_price": potential_price,
            "confidence": confidence,
            "sentiment": sentiment,
            "factors": factors,
            "timestamp": datetime.now().isoformat()
        }
    
    def identify_high_potential_coins(self, min_potential: float = 1.0, max_coins: int = 5) -> List[Dict[str, Any]]:
        """
        Identify cryptocurrencies with high growth potential
        
        Args:
            min_potential: Minimum growth potential multiple (e.g., 2.0 = 2x)
            max_coins: Maximum number of coins to return
            
        Returns:
            List of cryptocurrencies with high growth potential
        """
        results = []
        
        # Get trending coins as starting point
        trending = crypto_data_service.get_trending_coins()
        
        # Analyze each trending coin
        for coin in trending[:10]:  # Limit to top 10 trending
            symbol = coin.get("symbol", "").upper()
            if not symbol:
                continue
                
            # Analyze medium-term potential
            analysis = self.analyze_growth_potential(symbol, self.HORIZON_MEDIUM)
            
            # Filter by minimum potential
            if analysis.get("potential_multiple", 0) >= min_potential:
                results.append(analysis)
        
        # Sort by growth potential (descending)
        results.sort(key=lambda x: x.get("potential_multiple", 0), reverse=True)
        
        # Return top results
        return results[:max_coins]
    
    def format_prediction_for_query(self, query: str) -> str:
        """
        Format prediction data based on query with forced real-time data
        
        Args:
            query: User query about cryptocurrency predictions
            
        Returns:
            Formatted prediction data with real-time prices
        """
        query_lower = query.lower()
        
        # Extract time horizon from query
        time_horizon = self.HORIZON_MEDIUM  # Default
        if any(term in query_lower for term in ["short term", "short-term", "day", "week", "tomorrow"]):
            time_horizon = self.HORIZON_SHORT
        elif any(term in query_lower for term in ["long term", "long-term", "year", "future"]):
            time_horizon = self.HORIZON_LONG
        
        # Extract specific coins from query
        mentioned_coins = []
        coin_keywords = {
            'bitcoin': 'BTC', 'btc': 'BTC',
            'ethereum': 'ETH', 'eth': 'ETH',
            'solana': 'SOL', 'sol': 'SOL',
            'binance': 'BNB', 'bnb': 'BNB',
            'ripple': 'XRP', 'xrp': 'XRP',
            'cardano': 'ADA', 'ada': 'ADA',
            'dogecoin': 'DOGE', 'doge': 'DOGE'
        }
        
        for keyword, symbol in coin_keywords.items():
            if keyword in query_lower and symbol not in mentioned_coins:
                mentioned_coins.append(symbol)
        
        # Format response based on query type
        if "10x" in query_lower or "potential" in query_lower or "growth" in query_lower:
            # Query about high growth potential
            min_multiple = 10.0 if "10x" in query_lower else 2.0
            high_potential = self.identify_high_potential_coins(min_multiple)
            
            if high_potential:
                coins_data = []
                for coin in high_potential:
                    multiple = coin.get("potential_multiple", 0)
                    confidence = coin.get("confidence", self.CONFIDENCE_LOW)
                    coins_data.append(f"{coin['symbol']}: {multiple:.1f}x potential ({confidence} confidence)")
                
                return f"High potential cryptocurrencies ({time_horizon}):\\n" + "\\n".join(coins_data)
            else:
                return "No cryptocurrencies currently meet the high growth potential criteria."
        
        elif mentioned_coins:
            # Query about specific coins with forced real-time data
            analyses = []
            for symbol in mentioned_coins[:3]:  # Limit to 3 coins
                # Force real-time price data
                from direct_crypto_api import get_realtime_price
                realtime_data = get_realtime_price(symbol)
                
                if realtime_data:
                    # Use real-time price for display
                    realtime_price = realtime_data.get("price_usd", 0)
                    
                    # Get growth analysis
                    analysis = self.analyze_growth_potential(symbol, time_horizon)
                    if "error" not in analysis:
                        multiple = analysis.get("potential_multiple", 0)
                        confidence = analysis.get("confidence", self.CONFIDENCE_LOW)
                        
                        # Calculate potential price based on real-time price
                        potential_price = realtime_price * multiple
                        
                        # Include source for transparency
                        source = realtime_data.get("source", "API")
                        
                        analyses.append(f"{symbol}: Current ${realtime_price:.2f} → Potential ${potential_price:.2f} ({multiple:.1f}x, {confidence} confidence) [via {source}]")
                else:
                    # Fallback to regular analysis
                    analysis = self.analyze_growth_potential(symbol, time_horizon)
                    if "error" not in analysis:
                        multiple = analysis.get("potential_multiple", 0)
                        confidence = analysis.get("confidence", self.CONFIDENCE_LOW)
                        price = analysis.get("current_price", 0)
                        potential_price = analysis.get("potential_price", 0)
                        
                        analyses.append(f"{symbol}: Current ${price:.2f} → Potential ${potential_price:.2f} ({multiple:.1f}x, {confidence} confidence)")
            
            if analyses:
                current_time = datetime.now().strftime("%H:%M:%S UTC")
                return f"Cryptocurrency growth analysis ({time_horizon}) as of {current_time}:\\n" + "\\n".join(analyses)
            else:
                return "Unable to analyze the specified cryptocurrencies."
        
        else:
            # General market prediction with forced real-time data
            from direct_crypto_api import get_realtime_price
            
            # Get real-time BTC price
            btc_realtime = get_realtime_price("BTC")
            btc_price = btc_realtime.get("price_usd", 0) if btc_realtime else 0
            btc_source = btc_realtime.get("source", "API") if btc_realtime else "unknown"
            
            # Get real-time ETH price
            eth_realtime = get_realtime_price("ETH")
            eth_price = eth_realtime.get("price_usd", 0) if eth_realtime else 0
            eth_source = eth_realtime.get("source", "API") if eth_realtime else "unknown"
            
            # Get growth analysis
            btc_analysis = self.analyze_growth_potential("BTC", time_horizon)
            eth_analysis = self.analyze_growth_potential("ETH", time_horizon)
            
            # Get market overview
            market_overview = crypto_data_service.get_market_overview()
            market_cap = market_overview.get("total_market_cap_usd", 0) / 1e12  # In trillions
            
            # Calculate potential prices based on real-time prices
            btc_multiple = btc_analysis.get("potential_multiple", 0)
            eth_multiple = eth_analysis.get("potential_multiple", 0)
            
            btc_potential = btc_price * btc_multiple
            eth_potential = eth_price * eth_multiple
            
            current_time = datetime.now().strftime("%H:%M:%S UTC")
            return f"Crypto Market Forecast ({time_horizon}) as of {current_time}:\\n" + \
                   f"Total Market Cap: ${market_cap:.2f}T\\n" + \
                   f"BTC: Current ${btc_price:,.2f} → Potential ${btc_potential:,.2f} ({btc_multiple:.1f}x, {btc_analysis.get('confidence', 'low')} confidence) [via {btc_source}]\\n" + \
                   f"ETH: Current ${eth_price:,.2f} → Potential ${eth_potential:,.2f} ({eth_multiple:.1f}x, {eth_analysis.get('confidence', 'low')} confidence) [via {eth_source}]"

# Create singleton instance
crypto_prediction_engine = CryptoPredictionEngine()

def get_crypto_prediction(query: str) -> str:
    """Get cryptocurrency prediction data for a query"""
    return crypto_prediction_engine.format_prediction_for_query(query)

# Test function
if __name__ == "__main__":
    test_queries = [
        "Which cryptocurrencies have 10x potential in the next 90 days?",
        "What's the growth potential for Bitcoin and Ethereum?",
        "Predict the price of Solana in the long term",
        "What are the best crypto investments right now?"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Prediction: {get_crypto_prediction(query)}")