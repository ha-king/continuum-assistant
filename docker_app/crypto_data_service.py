"""
Crypto Data Service - Enhanced real-time cryptocurrency data access
"""

import requests
import json
import time
from typing import Dict, List, Optional, Any
from datetime import datetime
import os
from functools import lru_cache
from coinbase_api_service import coinbase_service, get_coinbase_price_data

class CryptoDataService:
    """Enhanced cryptocurrency data service with caching and multiple API sources"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 5  # Reduced timeout for faster responses
        self.cache_ttl = 60  # Cache TTL in seconds
        
        # API keys (would be stored in AWS Secrets Manager in production)
        self.coingecko_api_key = os.environ.get('COINGECKO_API_KEY', '')
        self.coinmarketcap_api_key = os.environ.get('COINMARKETCAP_API_KEY', '')
        
        # Top 100 cryptocurrencies by market cap (updated periodically)
        self.top_cryptos = [
            'BTC', 'ETH', 'USDT', 'BNB', 'SOL', 'XRP', 'USDC', 'ADA', 'DOGE', 'AVAX',
            'SHIB', 'DOT', 'TRX', 'LINK', 'TON', 'MATIC', 'WBTC', 'DAI', 'BCH', 'LTC'
        ]
    
    def get_crypto_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get cryptocurrency price with minimal caching for real-time data"""
        # Reduced cache TTL to ensure fresh data
        self.cache_ttl = 30  # 30 seconds max cache time
        
        # Force cache invalidation for critical requests
        self._price_cache = getattr(self, '_price_cache', {})
        cache_key = symbol.upper()
        
        # Check if we have a recent cache entry
        now = time.time()
        if cache_key in self._price_cache:
            timestamp, data = self._price_cache[cache_key]
            if now - timestamp < self.cache_ttl:
                return data
        
        # No valid cache entry, fetch fresh data
        result = None
        
        # Try Coinbase first (most reliable for major cryptos)
        result = self._fetch_from_coinbase(symbol)
        
        # Fallback to CoinGecko if Coinbase fails
        if not result:
            result = self._fetch_from_coingecko(symbol)
        
        # Fallback to CoinMarketCap if needed
        if not result:
            result = self._fetch_from_coinmarketcap(symbol)
        
        # Last resort fallback to Yahoo Finance
        if not result:
            result = self._fetch_from_yahoo(symbol)
        
        # Update cache with fresh data
        if result:
            self._price_cache[cache_key] = (now, result)
            
        return result
    
    def _fetch_from_coinbase(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch data from Coinbase API"""
        try:
            currency_pair = f"{symbol.upper()}-USD"
            
            # Get spot price
            spot_data = coinbase_service.get_spot_price(currency_pair)
            if not spot_data:
                return None
            
            # Get additional stats if available
            stats_data = coinbase_service.get_price_stats(currency_pair)
            
            price = spot_data['price']
            change_24h = 0
            volume_24h = 0
            
            if stats_data:
                if 'open' in stats_data and stats_data['open'] > 0:
                    change_24h = ((price - stats_data['open']) / stats_data['open']) * 100
                if 'volume' in stats_data:
                    volume_24h = stats_data['volume']
            
            return {
                'symbol': symbol.upper(),
                'name': f"{symbol.upper()}/USD",
                'price_usd': price,
                'change_24h': change_24h,
                'volume_24h': volume_24h,
                'timestamp': datetime.now().isoformat(),
                'source': 'coinbase'
            }
            
        except Exception as e:
            print(f"Coinbase API error: {str(e)}")
        
        return None
    
    def _fetch_from_coingecko(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch data from CoinGecko API with cache-busting"""
        try:
            coin_map = {
                'BTC': 'bitcoin', 'ETH': 'ethereum', 'SOL': 'solana',
                'BNB': 'binancecoin', 'XRP': 'ripple', 'ADA': 'cardano',
                'DOGE': 'dogecoin', 'AVAX': 'avalanche-2', 'SHIB': 'shiba-inu',
                'DOT': 'polkadot', 'TRX': 'tron', 'LINK': 'chainlink',
                'MATIC': 'matic-network', 'LTC': 'litecoin'
            }
            
            coin_id = coin_map.get(symbol.upper())
            if not coin_id:
                return None
            
            # Add timestamp to prevent caching
            timestamp = int(time.time())
            url = f"https://api.coingecko.com/api/v3/coins/{coin_id}?timestamp={timestamp}"
            if self.coingecko_api_key:
                url += f"&x_cg_pro_api_key={self.coingecko_api_key}"
            
            # Add cache control headers
            headers = {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                
                # Extract key metrics
                price = data['market_data']['current_price']['usd']
                change_24h = data['market_data']['price_change_percentage_24h'] or 0
                market_cap = data['market_data']['market_cap']['usd']
                volume_24h = data['market_data']['total_volume']['usd']
                
                # Get current time in ISO format with timezone
                current_time = datetime.now().isoformat()
                
                return {
                    'symbol': symbol.upper(),
                    'name': data['name'],
                    'price_usd': price,
                    'change_24h': change_24h,
                    'market_cap': market_cap,
                    'volume_24h': volume_24h,
                    'timestamp': current_time,
                    'source': 'coingecko'
                }
        except Exception as e:
            print(f"CoinGecko error: {str(e)}")
        
        return None
    
    def _fetch_from_coinmarketcap(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch data from CoinMarketCap API"""
        if not self.coinmarketcap_api_key:
            return None
            
        try:
            url = "https://pro-api.coinmarketcap.com/v1/cryptocurrency/quotes/latest"
            params = {
                'symbol': symbol.upper(),
                'convert': 'USD'
            }
            headers = {
                'X-CMC_PRO_API_KEY': self.coinmarketcap_api_key
            }
            
            response = self.session.get(url, params=params, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                quote_data = data['data'][symbol.upper()]['quote']['USD']
                
                return {
                    'symbol': symbol.upper(),
                    'name': data['data'][symbol.upper()]['name'],
                    'price_usd': quote_data['price'],
                    'change_24h': quote_data['percent_change_24h'] or 0,
                    'market_cap': quote_data['market_cap'],
                    'volume_24h': quote_data['volume_24h'],
                    'timestamp': datetime.now().isoformat(),
                    'source': 'coinmarketcap'
                }
        except Exception as e:
            print(f"CoinMarketCap error: {str(e)}")
            
        return None
    
    def _fetch_from_yahoo(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Fetch data from Yahoo Finance as last resort"""
        try:
            # Yahoo Finance uses -USD suffix for crypto
            url = f"https://query1.finance.yahoo.com/v8/finance/chart/{symbol.upper()}-USD"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                result = data['chart']['result'][0]
                meta = result['meta']
                
                return {
                    'symbol': symbol.upper(),
                    'name': f"{symbol.upper()}-USD",
                    'price_usd': meta['regularMarketPrice'],
                    'change_24h': (meta['regularMarketPrice'] - meta['chartPreviousClose']) / meta['chartPreviousClose'] * 100,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'yahoo'
                }
        except Exception as e:
            print(f"Yahoo Finance error: {str(e)}")
            
        return None
    
    def get_market_overview(self) -> Dict[str, Any]:
        """Get overall crypto market data"""
        try:
            url = "https://api.coingecko.com/api/v3/global"
            if self.coingecko_api_key:
                url += f"?x_cg_pro_api_key={self.coingecko_api_key}"
                
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()['data']
                
                return {
                    'total_market_cap_usd': data['total_market_cap']['usd'],
                    'total_volume_usd': data['total_volume']['usd'],
                    'btc_dominance': data['market_cap_percentage']['btc'],
                    'eth_dominance': data['market_cap_percentage']['eth'],
                    'active_cryptocurrencies': data['active_cryptocurrencies'],
                    'timestamp': datetime.now().isoformat()
                }
        except Exception as e:
            print(f"Market overview error: {str(e)}")
            
        return {
            'timestamp': datetime.now().isoformat(),
            'error': 'Unable to fetch market overview'
        }
    
    def get_trending_coins(self) -> List[Dict[str, Any]]:
        """Get trending cryptocurrencies"""
        try:
            url = "https://api.coingecko.com/api/v3/search/trending"
            if self.coingecko_api_key:
                url += f"?x_cg_pro_api_key={self.coingecko_api_key}"
                
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                coins = data['coins']
                
                return [
                    {
                        'id': coin['item']['id'],
                        'name': coin['item']['name'],
                        'symbol': coin['item']['symbol'],
                        'market_cap_rank': coin['item']['market_cap_rank']
                    }
                    for coin in coins[:5]  # Limit to top 5
                ]
        except Exception as e:
            print(f"Trending coins error: {str(e)}")
            
        return []
    
    def format_crypto_data_for_context(self, query: str) -> str:
        """Format cryptocurrency data for context enhancement"""
        # Extract mentioned crypto symbols
        query_lower = query.lower()
        mentioned_symbols = []
        
        crypto_keywords = {
            'bitcoin': 'BTC', 'btc': 'BTC',
            'ethereum': 'ETH', 'eth': 'ETH',
            'solana': 'SOL', 'sol': 'SOL',
            'binance': 'BNB', 'bnb': 'BNB',
            'ripple': 'XRP', 'xrp': 'XRP',
            'cardano': 'ADA', 'ada': 'ADA',
            'dogecoin': 'DOGE', 'doge': 'DOGE'
        }
        
        for keyword, symbol in crypto_keywords.items():
            if keyword in query_lower and symbol not in mentioned_symbols:
                mentioned_symbols.append(symbol)
        
        # If no specific cryptos mentioned but query is about crypto,
        # include top coins
        if not mentioned_symbols and any(word in query_lower for word in 
                                         ['crypto', 'cryptocurrency', 'token', 'coin', 'blockchain']):
            mentioned_symbols = self.top_cryptos[:3]  # Top 3 cryptos
        
        # Get data for mentioned symbols
        crypto_data = []
        for symbol in mentioned_symbols[:5]:  # Limit to 5 cryptos
            data = self.get_crypto_price(symbol)
            if data:
                crypto_data.append(data)
        
        # Format the data
        if crypto_data:
            lines = []
            for data in crypto_data:
                price_str = f"${data['price_usd']:,.4f}" if data['price_usd'] < 1 else f"${data['price_usd']:,.2f}"
                change_str = f"{data['change_24h']:+.2f}%" if 'change_24h' in data else "N/A"
                lines.append(f"{data['symbol']}: {price_str} ({change_str})")
            
            # Add market overview if query is about the overall market
            if any(word in query_lower for word in ['market', 'overall', 'trend']):
                try:
                    overview = self.get_market_overview()
                    if 'total_market_cap_usd' in overview:
                        market_cap_str = f"${overview['total_market_cap_usd']/1e12:.2f}T"
                        btc_dom_str = f"{overview['btc_dominance']:.1f}%"
                        lines.append(f"Total Market Cap: {market_cap_str} | BTC Dominance: {btc_dom_str}")
                except:
                    pass
                    
            return " | ".join(lines)
        
        return "No specific cryptocurrency data available"

# Create singleton instance
crypto_data_service = CryptoDataService()

def get_enhanced_crypto_data(query: str) -> str:
    """Get enhanced cryptocurrency data for a query with Coinbase integration"""
    try:
        # Try Coinbase first for real-time data
        coinbase_data = get_coinbase_price_data(query)
        if coinbase_data and "Error" not in coinbase_data and "unavailable" not in coinbase_data:
            # Add timestamp and source info
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
            return f"{coinbase_data} | Source: Coinbase API | Time: {timestamp}"
    except Exception as e:
        print(f"Coinbase integration error: {str(e)}")
    
    # Fallback to existing service
    fallback_data = crypto_data_service.format_crypto_data_for_context(query)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC")
    return f"{fallback_data} | Time: {timestamp}"

# Test function
if __name__ == "__main__":
    test_queries = [
        "What's the current price of Bitcoin?",
        "Compare Ethereum and Solana performance",
        "What are the trending cryptocurrencies?",
        "Analyze the overall crypto market conditions"
    ]
    
    for query in test_queries:
        print(f"\nQuery: {query}")
        print(f"Data: {get_enhanced_crypto_data(query)}")