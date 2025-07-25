"""
Coinbase API Service - Real-time and historical cryptocurrency data access
"""

import boto3
import json
import requests
import time
import hmac
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Any
from functools import lru_cache

class CoinbaseAPIService:
    """Coinbase API service for real-time and historical crypto data"""
    
    def __init__(self, region_name='us-west-2'):
        self.region_name = region_name
        self.base_url = "https://api.coinbase.com/v2"
        self.pro_base_url = "https://api.exchange.coinbase.com"
        self.session = requests.Session()
        self.timeout = 10
        
        # Initialize credentials
        self.api_key = None
        self.api_secret = None
        self._load_credentials()
    
    def _load_credentials(self):
        """Load Coinbase API credentials from AWS Secrets Manager"""
        try:
            secrets_client = boto3.client('secretsmanager', region_name=self.region_name)
            
            # Get API key
            try:
                key_response = secrets_client.get_secret_value(SecretId='coinbase-api-key')
                self.api_key = key_response['SecretString'].strip()
                if self.api_key:
                    print("✓ Coinbase API key loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load coinbase-api-key: {e}")
                self.api_key = None
            
            # Get API secret/token
            try:
                secret_response = secrets_client.get_secret_value(SecretId='coinbase-api-token')
                self.api_secret = secret_response['SecretString'].strip()
                if self.api_secret:
                    print("✓ Coinbase API secret loaded successfully")
            except Exception as e:
                print(f"Warning: Could not load coinbase-api-token: {e}")
                self.api_secret = None
                
        except Exception as e:
            print(f"Error loading Coinbase credentials: {e}")
            self.api_key = None
            self.api_secret = None
    
    def _create_auth_headers(self, method: str, path: str, body: str = '') -> Dict[str, str]:
        """Create authentication headers for Coinbase Pro API"""
        if not self.api_key or not self.api_secret:
            return {}
        
        timestamp = str(int(time.time()))
        message = timestamp + method + path + body
        
        try:
            signature = hmac.new(
                base64.b64decode(self.api_secret),
                message.encode('utf-8'),
                hashlib.sha256
            ).digest()
            signature_b64 = base64.b64encode(signature).decode()
            
            return {
                'CB-ACCESS-KEY': self.api_key,
                'CB-ACCESS-SIGN': signature_b64,
                'CB-ACCESS-TIMESTAMP': timestamp,
                'CB-ACCESS-PASSPHRASE': 'your-passphrase',  # This would also be in secrets
                'Content-Type': 'application/json'
            }
        except Exception as e:
            print(f"Error creating auth headers: {e}")
            return {}
    
    def get_spot_price(self, currency_pair: str = 'BTC-USD') -> Optional[Dict[str, Any]]:
        """Get current spot price for a currency pair"""
        try:
            # Try the public exchange rates endpoint first
            url = f"{self.base_url}/exchange-rates"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'rates' in data['data']:
                    rates = data['data']['rates']
                    
                    # Extract base currency from pair
                    base_currency = currency_pair.split('-')[0]
                    
                    if base_currency in rates:
                        price = float(rates[base_currency])
                        # Convert from rate to price (rates are inverted)
                        if price > 0:
                            price = 1.0 / price
                        
                        return {
                            'currency_pair': currency_pair,
                            'price': price,
                            'timestamp': datetime.now().isoformat(),
                            'source': 'coinbase_public'
                        }
            
            # Fallback: Try the prices endpoint
            base_currency = currency_pair.split('-')[0]
            url = f"{self.base_url}/prices/{base_currency}-USD/spot"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'amount' in data['data']:
                    return {
                        'currency_pair': currency_pair,
                        'price': float(data['data']['amount']),
                        'timestamp': datetime.now().isoformat(),
                        'source': 'coinbase_spot'
                    }
                    
        except Exception as e:
            print(f"Error fetching spot price for {currency_pair}: {e}")
        
        return None
    
    def get_current_prices(self, symbols: List[str]) -> Dict[str, Any]:
        """Get current prices for multiple cryptocurrencies"""
        prices = {}
        
        for symbol in symbols:
            currency_pair = f"{symbol.upper()}-USD"
            price_data = self.get_spot_price(currency_pair)
            if price_data:
                prices[symbol.upper()] = price_data
        
        return prices
    
    def get_historical_prices(self, currency_pair: str = 'BTC-USD', 
                            days: int = 30) -> Optional[List[Dict[str, Any]]]:
        """Get historical price data"""
        try:
            # Use public API for historical data
            base_currency = currency_pair.split('-')[0]
            url = f"{self.base_url}/prices/{base_currency}-USD/historic"
            
            # Calculate date range
            end_date = datetime.now()
            start_date = end_date - timedelta(days=days)
            
            params = {
                'period': 'day'
            }
            
            response = self.session.get(url, params=params, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'prices' in data['data']:
                    prices = data['data']['prices']
                    
                    # Convert to more usable format and limit to requested days
                    historical_data = []
                    for price_point in prices[-days:]:  # Get last N days
                        historical_data.append({
                            'date': price_point['time'],
                            'price': float(price_point['price']),
                            'currency_pair': currency_pair
                        })
                    
                    return historical_data
                    
        except Exception as e:
            print(f"Error fetching historical prices for {currency_pair}: {e}")
        
        return None
    
    def get_price_stats(self, currency_pair: str = 'BTC-USD') -> Optional[Dict[str, Any]]:
        """Get 24hr price statistics"""
        try:
            # Try to use Pro API if authenticated
            if self.api_key and self.api_secret:
                path = f"/products/{currency_pair}/stats"
                headers = self._create_auth_headers('GET', path)
                url = f"{self.pro_base_url}{path}"
                
                response = self.session.get(url, headers=headers, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json()
                    return {
                        'currency_pair': currency_pair,
                        'open': float(data.get('open', 0)),
                        'high': float(data.get('high', 0)),
                        'low': float(data.get('low', 0)),
                        'volume': float(data.get('volume', 0)),
                        'last': float(data.get('last', 0)),
                        'timestamp': datetime.now().isoformat(),
                        'source': 'coinbase_pro'
                    }
            
            # Fallback to basic price data
            spot_price = self.get_spot_price(currency_pair)
            if spot_price:
                return {
                    'currency_pair': currency_pair,
                    'last': spot_price['price'],
                    'timestamp': spot_price['timestamp'],
                    'source': 'coinbase_basic'
                }
                
        except Exception as e:
            print(f"Error fetching price stats: {e}")
        
        return None
    
    def get_market_data(self, symbols: List[str] = None) -> Dict[str, Any]:
        """Get comprehensive market data for specified symbols"""
        if symbols is None:
            symbols = ['BTC', 'ETH', 'SOL', 'ADA', 'DOT']
        
        market_data = {
            'timestamp': datetime.now().isoformat(),
            'prices': {},
            'stats': {}
        }
        
        for symbol in symbols:
            currency_pair = f"{symbol.upper()}-USD"
            
            # Get current price
            price_data = self.get_spot_price(currency_pair)
            if price_data:
                market_data['prices'][symbol] = price_data
            
            # Get price statistics
            stats_data = self.get_price_stats(currency_pair)
            if stats_data:
                market_data['stats'][symbol] = stats_data
        
        return market_data
    
    def format_price_data(self, symbol: str) -> str:
        """Format price data for display in assistant responses"""
        try:
            currency_pair = f"{symbol.upper()}-USD"
            
            # Get current price and stats
            price_data = self.get_spot_price(currency_pair)
            stats_data = self.get_price_stats(currency_pair)
            
            if not price_data:
                return f"{symbol.upper()}: Price data unavailable"
            
            price_str = f"${price_data['price']:,.2f}"
            
            if stats_data and 'open' in stats_data and stats_data['open'] > 0:
                change = ((price_data['price'] - stats_data['open']) / stats_data['open']) * 100
                change_str = f" ({change:+.2f}%)"
                
                if 'high' in stats_data and 'low' in stats_data:
                    range_str = f" | 24h Range: ${stats_data['low']:,.2f} - ${stats_data['high']:,.2f}"
                else:
                    range_str = ""
                
                return f"{symbol.upper()}: {price_str}{change_str}{range_str}"
            else:
                return f"{symbol.upper()}: {price_str}"
                
        except Exception as e:
            return f"{symbol.upper()}: Error fetching price data - {str(e)}"
    
    def get_trending_analysis(self, symbols: List[str], days: int = 7) -> str:
        """Get trending analysis for multiple symbols"""
        analysis_parts = []
        
        for symbol in symbols:
            try:
                # Get historical data for trend analysis
                historical = self.get_historical_prices(f"{symbol.upper()}-USD", days)
                current_price = self.get_spot_price(f"{symbol.upper()}-USD")
                
                if historical and current_price and len(historical) >= 2:
                    start_price = historical[0]['price']
                    end_price = current_price['price']
                    change = ((end_price - start_price) / start_price) * 100
                    
                    trend = "📈" if change > 0 else "📉"
                    analysis_parts.append(f"{symbol.upper()}: {trend} {change:+.1f}% ({days}d)")
                else:
                    formatted_price = self.format_price_data(symbol)
                    analysis_parts.append(formatted_price)
                    
            except Exception as e:
                analysis_parts.append(f"{symbol.upper()}: Analysis error")
        
        return " | ".join(analysis_parts)

# Create singleton instance
coinbase_service = CoinbaseAPIService()

def get_coinbase_price_data(query: str) -> str:
    """Get Coinbase price data based on query context"""
    query_lower = query.lower()
    
    # Extract mentioned cryptocurrencies
    crypto_symbols = []
    crypto_keywords = {
        'bitcoin': 'BTC', 'btc': 'BTC',
        'ethereum': 'ETH', 'eth': 'ETH', 
        'solana': 'SOL', 'sol': 'SOL',
        'cardano': 'ADA', 'ada': 'ADA',
        'polkadot': 'DOT', 'dot': 'DOT'
    }
    
    for keyword, symbol in crypto_keywords.items():
        if keyword in query_lower and symbol not in crypto_symbols:
            crypto_symbols.append(symbol)
    
    # Default to major cryptos if none specified
    if not crypto_symbols:
        crypto_symbols = ['BTC', 'ETH', 'SOL']
    
    # Check if historical analysis is requested
    if any(word in query_lower for word in ['trend', 'historical', 'week', 'month', 'performance']):
        days = 7
        if 'month' in query_lower:
            days = 30
        elif 'week' in query_lower:
            days = 7
        
        return coinbase_service.get_trending_analysis(crypto_symbols, days)
    else:
        # Get current price data
        price_data = []
        for symbol in crypto_symbols[:5]:  # Limit to 5 symbols
            formatted_price = coinbase_service.format_price_data(symbol)
            price_data.append(formatted_price)
        
        return " | ".join(price_data)

# Test function
if __name__ == "__main__":
    # Test the service
    service = CoinbaseAPIService()
    
    print("Testing Coinbase API Service:")
    print("1. BTC Spot Price:", service.get_spot_price('BTC-USD'))
    print("2. ETH Price Stats:", service.get_price_stats('ETH-USD'))
    print("3. Market Data:", service.get_market_data(['BTC', 'ETH']))
    print("4. Formatted BTC:", service.format_price_data('BTC'))