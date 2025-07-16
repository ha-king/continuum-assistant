"""
Centralized Real-Time Data Access Module for Continuum Assistant
Provides unified access to live data sources for all assistants
"""

import requests
import json
import re
from datetime import datetime
from typing import Dict, List, Optional, Any
import urllib.parse

class RealTimeDataAccess:
    """Centralized real-time data access for all assistants"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })
        self.timeout = 10
        
    def get_current_datetime(self) -> str:
        """Get current datetime formatted for context"""
        return datetime.now().strftime("%A, %B %d, %Y at %I:%M %p UTC")
    
    def enhance_query_with_realtime_context(self, query: str, assistant_type: str = "general") -> str:
        """Add real-time context to any query"""
        context = f"CURRENT DATE/TIME: {self.get_current_datetime()}\n\n"
        
        # Get relevant real-time data based on query content
        realtime_data = self.get_relevant_realtime_data(query, assistant_type)
        if realtime_data:
            context += f"LIVE DATA:\n{realtime_data}\n\n"
        
        return f"{context}Query: {query}"
    
    def get_relevant_realtime_data(self, query: str, assistant_type: str) -> str:
        """Get relevant real-time data based on query content and assistant type"""
        data_parts = []
        query_lower = query.lower()
        
        # Financial/Crypto data
        if any(word in query_lower for word in ['price', 'crypto', 'bitcoin', 'ethereum', 'stock', 'market']):
            crypto_data = self.get_crypto_prices(query)
            if crypto_data:
                data_parts.append(f"CRYPTO PRICES: {crypto_data}")
        
        # F1/Sports data
        if any(word in query_lower for word in ['f1', 'formula', 'race', 'grand prix', 'motorsport']):
            f1_data = self.get_f1_data()
            if f1_data:
                data_parts.append(f"F1 DATA: {f1_data}")
        
        # Weather data for location-based queries
        if any(word in query_lower for word in ['weather', 'temperature', 'forecast']):
            weather_data = self.get_weather_data(query)
            if weather_data:
                data_parts.append(f"WEATHER: {weather_data}")
        
        # News/Current events
        if any(word in query_lower for word in ['news', 'current', 'latest', 'today', 'recent']):
            news_data = self.get_current_news(query)
            if news_data:
                data_parts.append(f"CURRENT NEWS: {news_data}")
        
        # Web/Company data
        if any(domain in query_lower for domain in ['.com', '.org', '.net', 'website', 'company']):
            web_data = self.get_web_data(query)
            if web_data:
                data_parts.append(f"WEB DATA: {web_data}")
        
        # AWS/Tech updates
        if assistant_type == "aws" or any(word in query_lower for word in ['aws', 'amazon web services', 'cloud']):
            aws_data = self.get_aws_updates()
            if aws_data:
                data_parts.append(f"AWS UPDATES: {aws_data}")
        
        return "\n\n".join(data_parts)
    
    def get_crypto_prices(self, query: str) -> Optional[str]:
        """Get cryptocurrency prices from multiple sources"""
        crypto_symbols = {
            'bitcoin': 'BTC', 'btc': 'BTC',
            'ethereum': 'ETH', 'eth': 'ETH', 
            'apecoin': 'APE', 'ape': 'APE',
            'dogecoin': 'DOGE', 'doge': 'DOGE',
            'cardano': 'ADA', 'ada': 'ADA',
            'solana': 'SOL', 'sol': 'SOL',
            'chainlink': 'LINK', 'link': 'LINK',
            'polygon': 'MATIC', 'matic': 'MATIC'
        }
        
        prices = []
        query_lower = query.lower()
        
        for name, symbol in crypto_symbols.items():
            if name in query_lower:
                price = self._fetch_crypto_price(symbol)
                if price:
                    prices.append(f"{symbol}: {price}")
        
        return " | ".join(prices) if prices else None
    
    def _fetch_crypto_price(self, symbol: str) -> Optional[str]:
        """Fetch individual crypto price"""
        try:
            # Try CoinGecko API
            coin_map = {
                'BTC': 'bitcoin', 'ETH': 'ethereum', 'APE': 'apecoin',
                'DOGE': 'dogecoin', 'ADA': 'cardano', 'SOL': 'solana',
                'LINK': 'chainlink', 'MATIC': 'matic-network'
            }
            
            coin_id = coin_map.get(symbol)
            if coin_id:
                url = f"https://api.coingecko.com/api/v3/simple/price?ids={coin_id}&vs_currencies=usd&include_24hr_change=true"
                response = self.session.get(url, timeout=self.timeout)
                
                if response.status_code == 200:
                    data = response.json().get(coin_id, {})
                    if data:
                        price = data.get('usd', 0)
                        change = data.get('usd_24h_change', 0)
                        return f"${price:,.4f} ({change:+.2f}%)"
        except:
            pass
        
        return None
    
    def get_f1_data(self) -> Optional[str]:
        """Get current F1 race information"""
        try:
            # Try Ergast API for F1 data
            url = "https://ergast.com/api/f1/current/next.json"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
                if races:
                    race = races[0]
                    race_name = race.get('raceName', 'Unknown')
                    circuit = race.get('Circuit', {}).get('circuitName', 'Unknown')
                    date = race.get('date', 'TBD')
                    return f"Next: {race_name} at {circuit} on {date}"
        except:
            pass
        
        return f"F1 Season {datetime.now().year} - Check official sources for current race schedule"
    
    def get_weather_data(self, query: str) -> Optional[str]:
        """Get weather data (placeholder - would need API key)"""
        # This would require a weather API key like OpenWeatherMap
        # For now, return guidance
        return "Weather data requires API integration - check local weather services"
    
    def get_current_news(self, query: str) -> Optional[str]:
        """Get current news (simplified implementation)"""
        try:
            # Try to get news from a simple RSS or public API
            # This is a simplified implementation
            return f"Current news as of {self.get_current_datetime()} - Check major news sources for latest updates"
        except:
            pass
        
        return None
    
    def get_web_data(self, query: str) -> Optional[str]:
        """Get web data from URLs or company websites"""
        urls = self._extract_urls(query)
        
        if not urls:
            # Look for company names and construct URLs
            if 'infascination' in query.lower():
                urls = ['https://infascination.com']
        
        results = []
        for url in urls[:2]:  # Limit to 2 URLs
            try:
                web_info = self._fetch_website_info(url)
                if web_info:
                    results.append(web_info)
            except:
                continue
        
        return " | ".join(results) if results else None
    
    def _extract_urls(self, query: str) -> List[str]:
        """Extract URLs from query"""
        url_pattern = r'https?://[^\s<>"{}|\\^`\[\]]+'
        urls = re.findall(url_pattern, query)
        
        # Also look for domain patterns
        domain_pattern = r'\b[a-zA-Z0-9-]+\.[a-zA-Z]{2,}\b'
        domains = re.findall(domain_pattern, query)
        
        for domain in domains:
            if not domain.startswith('http') and '.' in domain:
                urls.append(f"https://{domain}")
        
        return list(set(urls))
    
    def _fetch_website_info(self, url: str) -> Optional[str]:
        """Fetch basic website information"""
        try:
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                content = response.text
                
                # Extract title
                title_match = re.search(r'<title[^>]*>(.*?)</title>', content, re.IGNORECASE | re.DOTALL)
                title = "Unknown"
                if title_match:
                    title = re.sub(r'<[^>]+>', '', title_match.group(1)).strip()[:100]
                
                return f"{url}: {title} (Status: {response.status_code})"
        except:
            pass
        
        return None
    
    def get_aws_updates(self) -> Optional[str]:
        """Get AWS service updates and announcements"""
        try:
            # This would ideally connect to AWS What's New RSS or API
            return f"AWS Updates as of {self.get_current_datetime()} - Check AWS What's New for latest service announcements"
        except:
            pass
        
        return None
    
    def get_market_data(self, query: str) -> Optional[str]:
        """Get general market data"""
        try:
            # This would connect to financial APIs for stock market data
            return f"Market data as of {self.get_current_datetime()} - Check financial data providers for current market information"
        except:
            pass
        
        return None

# Global instance for all assistants to use
realtime_data = RealTimeDataAccess()

def enhance_query_with_realtime(query: str, assistant_type: str = "general") -> str:
    """Convenience function for assistants to enhance queries with real-time data"""
    return realtime_data.enhance_query_with_realtime_context(query, assistant_type)

def get_current_datetime() -> str:
    """Get current datetime for assistants"""
    return realtime_data.get_current_datetime()