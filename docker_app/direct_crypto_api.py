"""
Direct Crypto API - Immediate access to cryptocurrency prices without caching
"""

import requests
import time
from datetime import datetime
from typing import Dict, Any, Optional

class DirectCryptoAPI:
    """Direct API access to cryptocurrency prices without caching"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 3  # Short timeout for fast responses
    
    def get_current_price(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Get current price directly from API without caching"""
        # Try multiple sources in parallel for speed and reliability
        result = self._try_binance_api(symbol)
        if not result:
            result = self._try_coingecko_api(symbol)
        if not result:
            result = self._try_coinbase_api(symbol)
            
        return result
    
    def _try_binance_api(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Try Binance API for real-time price data"""
        try:
            # Convert symbol to Binance format
            ticker = f"{symbol.upper()}USDT"
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={ticker}"
            
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                price = float(data.get('price', 0))
                
                # Get 24h change from ticker
                ticker_url = f"https://api.binance.com/api/v3/ticker/24hr?symbol={ticker}"
                ticker_response = self.session.get(ticker_url, timeout=self.timeout)
                change_24h = 0
                
                if ticker_response.status_code == 200:
                    ticker_data = ticker_response.json()
                    price_change = float(ticker_data.get('priceChangePercent', 0))
                    change_24h = price_change
                
                return {
                    'symbol': symbol.upper(),
                    'price_usd': price,
                    'change_24h': change_24h,
                    'timestamp': datetime.now().isoformat(),
                    'source': 'binance'
                }
        except Exception as e:
            print(f"Binance API error: {str(e)}")
        
        return None
    
    def _try_coingecko_api(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Try CoinGecko API for price data"""
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
            url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true&t={timestamp}"
            
            # Add cache control headers
            headers = {
                'Cache-Control': 'no-cache, no-store, must-revalidate',
                'Pragma': 'no-cache',
                'Expires': '0'
            }
            
            response = self.session.get(url, headers=headers, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json().get(coin_id, {})
                if data:
                    price = data.get('usd', 0)
                    change_24h = data.get('usd_24h_change', 0)
                    
                    return {
                        'symbol': symbol.upper(),
                        'price_usd': price,
                        'change_24h': change_24h,
                        'timestamp': datetime.now().isoformat(),
                        'source': 'coingecko'
                    }
        except Exception as e:
            print(f"CoinGecko API error: {str(e)}")
        
        return None
    
    def _try_coinbase_api(self, symbol: str) -> Optional[Dict[str, Any]]:
        """Try Coinbase API for price data"""
        try:
            ticker = f"{symbol.upper()}-USD"
            url = f"https://api.coinbase.com/v2/prices/{ticker}/spot"
            
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json().get('data', {})
                if data:
                    price = float(data.get('amount', 0))
                    
                    return {
                        'symbol': symbol.upper(),
                        'price_usd': price,
                        'change_24h': 0,  # Coinbase doesn't provide 24h change in this endpoint
                        'timestamp': datetime.now().isoformat(),
                        'source': 'coinbase'
                    }
        except Exception as e:
            print(f"Coinbase API error: {str(e)}")
        
        return None

# Create singleton instance
direct_crypto_api = DirectCryptoAPI()

def get_realtime_price(symbol: str) -> Optional[Dict[str, Any]]:
    """Get real-time price for a cryptocurrency symbol"""
    return direct_crypto_api.get_current_price(symbol)