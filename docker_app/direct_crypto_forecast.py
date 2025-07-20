"""
Direct Crypto Forecast - Complete bypass for crypto price forecasting
"""

import requests
import time
import json
from datetime import datetime
from typing import Dict, Any, List

class DirectCryptoForecast:
    """Direct cryptocurrency forecasting with no caching"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 2  # Very short timeout
        
        # Confidence levels
        self.CONFIDENCE_LOW = "low"
        self.CONFIDENCE_MEDIUM = "medium"
        self.CONFIDENCE_HIGH = "high"
        
        # Time horizons
        self.HORIZON_SHORT = "short-term"  # Days to weeks
        self.HORIZON_MEDIUM = "medium-term"  # Weeks to months
        self.HORIZON_LONG = "long-term"  # Months+
    
    def get_direct_price(self, symbol: str) -> Dict[str, Any]:
        """Get price directly from exchange APIs"""
        # Try multiple sources in parallel for speed
        for source_func in [self._get_binance_price, self._get_coinbase_price, self._get_coingecko_price]:
            try:
                result = source_func(symbol)
                if result and result.get('price_usd', 0) > 0:
                    return result
            except:
                continue
        
        # Fallback with error
        return {
            'symbol': symbol,
            'price_usd': 0,
            'error': True,
            'timestamp': datetime.now().isoformat()
        }
    
    def _get_binance_price(self, symbol: str) -> Dict[str, Any]:
        """Get price from Binance"""
        ticker = f"{symbol.upper()}USDT"
        url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}&_={int(time.time() * 1000)}"
        
        response = self.session.get(url, timeout=self.timeout)
        if response.status_code == 200:
            data = response.json()
            price = float(data.get('price', 0))
            
            return {
                'symbol': symbol.upper(),
                'price_usd': price,
                'source': 'binance',
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def _get_coinbase_price(self, symbol: str) -> Dict[str, Any]:
        """Get price from Coinbase"""
        ticker = f"{symbol.upper()}-USD"
        url = f"https://api.coinbase.com/v2/prices/{ticker}/spot?_={int(time.time() * 1000)}"
        
        response = self.session.get(url, timeout=self.timeout)
        if response.status_code == 200:
            data = response.json().get('data', {})
            price = float(data.get('amount', 0))
            
            return {
                'symbol': symbol.upper(),
                'price_usd': price,
                'source': 'coinbase',
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def _get_coingecko_price(self, symbol: str) -> Dict[str, Any]:
        """Get price from CoinGecko"""
        coin_map = {
            'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
            'BNB': 'binancecoin', 'XRP': 'ripple', 'ADA': 'cardano',
            'DOGE': 'dogecoin', 'AVAX': 'avalanche-2', 'SHIB': 'shiba-inu'
        }
        
        coin_id = coin_map.get(symbol.upper())
        if not coin_id:
            return None
            
        url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&_={int(time.time() * 1000)}"
        
        response = self.session.get(url, timeout=self.timeout)
        if response.status_code == 200:
            data = response.json().get(coin_id, {})
            price = data.get('usd', 0)
            
            return {
                'symbol': symbol.upper(),
                'price_usd': price,
                'source': 'coingecko',
                'timestamp': datetime.now().isoformat()
            }
        return None
    
    def get_growth_potential(self, symbol: str, time_horizon: str) -> Dict[str, Any]:
        """Calculate growth potential based on market cap and time horizon"""
        # Get current price
        price_data = self.get_direct_price(symbol)
        if price_data.get('error', False) or price_data.get('price_usd', 0) == 0:
            return {
                'symbol': symbol,
                'error': True,
                'message': 'Unable to retrieve current price'
            }
        
        # Get market cap (simplified approach)
        market_cap = self._estimate_market_cap(symbol)
        
        # Default values
        growth_potential = 0
        confidence = self.CONFIDENCE_MEDIUM
        
        # Calculate based on market cap and time horizon
        if market_cap > 100_000_000_000:  # $100B+
            confidence = self.CONFIDENCE_HIGH
            if time_horizon == self.HORIZON_SHORT:
                growth_potential = 0.2  # 20% potential
            elif time_horizon == self.HORIZON_MEDIUM:
                growth_potential = 0.5  # 50% potential
            else:
                growth_potential = 1.0  # 100% potential (2x)
        elif market_cap > 10_000_000_000:  # $10B+
            confidence = self.CONFIDENCE_MEDIUM
            if time_horizon == self.HORIZON_SHORT:
                growth_potential = 0.3  # 30% potential
            elif time_horizon == self.HORIZON_MEDIUM:
                growth_potential = 1.0  # 100% potential (2x)
            else:
                growth_potential = 3.0  # 300% potential (4x)
        else:
            confidence = self.CONFIDENCE_LOW
            if time_horizon == self.HORIZON_SHORT:
                growth_potential = 0.5  # 50% potential
            elif time_horizon == self.HORIZON_MEDIUM:
                growth_potential = 2.0  # 200% potential (3x)
            else:
                growth_potential = 9.0  # 900% potential (10x)
        
        # Calculate potential price
        current_price = price_data.get('price_usd', 0)
        potential_price = current_price * (1 + growth_potential)
        
        return {
            'symbol': symbol,
            'current_price': current_price,
            'potential_price': potential_price,
            'growth_potential': growth_potential,
            'multiple': 1 + growth_potential,
            'confidence': confidence,
            'source': price_data.get('source', 'unknown'),
            'timestamp': datetime.now().isoformat()
        }
    
    def _estimate_market_cap(self, symbol: str) -> float:
        """Estimate market cap based on symbol"""
        # Simplified market cap estimates
        estimates = {
            'BTC': 1_200_000_000_000,  # $1.2T
            'ETH': 350_000_000_000,    # $350B
            'SOL': 70_000_000_000,     # $70B
            'BNB': 60_000_000_000,     # $60B
            'XRP': 30_000_000_000,     # $30B
            'ADA': 15_000_000_000,     # $15B
            'DOGE': 12_000_000_000,    # $12B
            'AVAX': 10_000_000_000,    # $10B
            'SHIB': 8_000_000_000      # $8B
        }
        
        return estimates.get(symbol.upper(), 5_000_000_000)  # Default $5B
    
    def generate_forecast_response(self, query: str) -> str:
        """Generate forecast response based on query"""
        query_lower = query.lower()
        
        # Extract time horizon
        time_horizon = self.HORIZON_MEDIUM  # Default
        if any(term in query_lower for term in ["short term", "short-term", "day", "week", "tomorrow"]):
            time_horizon = self.HORIZON_SHORT
        elif any(term in query_lower for term in ["long term", "long-term", "year", "future"]):
            time_horizon = self.HORIZON_LONG
        
        # Extract mentioned coins
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
        
        # If no specific coins mentioned, use BTC and ETH
        if not mentioned_coins:
            mentioned_coins = ['BTC', 'ETH']
        
        # Generate forecasts
        forecasts = []
        for symbol in mentioned_coins[:3]:  # Limit to 3 coins
            analysis = self.get_growth_potential(symbol, time_horizon)
            if not analysis.get('error', False):
                current_price = analysis.get('current_price', 0)
                potential_price = analysis.get('potential_price', 0)
                multiple = analysis.get('multiple', 0)
                confidence = analysis.get('confidence', self.CONFIDENCE_LOW)
                source = analysis.get('source', 'unknown')
                
                # Format price based on value
                if current_price >= 1000:
                    current_price_str = f"${current_price:,.0f}"
                    potential_price_str = f"${potential_price:,.0f}"
                elif current_price >= 1:
                    current_price_str = f"${current_price:,.2f}"
                    potential_price_str = f"${potential_price:,.2f}"
                else:
                    current_price_str = f"${current_price:,.4f}"
                    potential_price_str = f"${potential_price:,.4f}"
                
                forecasts.append(f"{symbol}: Current {current_price_str} → Potential {potential_price_str} ({multiple:.1f}x, {confidence} confidence) [via {source}]")
        
        # Format response
        current_time = datetime.now().strftime("%H:%M:%S UTC")
        if forecasts:
            return f"DIRECT CRYPTO FORECAST ({time_horizon}) as of {current_time}:\n" + "\n".join(forecasts)
        else:
            return f"Unable to generate crypto forecast at {current_time}. Please try again."

# Create singleton instance
direct_forecaster = DirectCryptoForecast()

def get_direct_forecast(query: str) -> str:
    """Get direct crypto forecast with no caching"""
    return direct_forecaster.generate_forecast_response(query)