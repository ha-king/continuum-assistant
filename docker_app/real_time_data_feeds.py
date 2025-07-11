import requests
import json
from datetime import datetime
import asyncio
import aiohttp

class RealTimeDataFeeds:
    def __init__(self):
        self.api_keys = {
            'coingecko': 'demo-api-key',  # Replace with actual API key
            'alpha_vantage': 'demo',      # Replace with actual API key
            'news_api': 'demo'            # Replace with actual API key
        }
        self.base_urls = {
            'coingecko': 'https://api.coingecko.com/api/v3',
            'alpha_vantage': 'https://www.alphavantage.co/query',
            'news_api': 'https://newsapi.org/v2',
            'yahoo_finance': 'https://query1.finance.yahoo.com/v8/finance/chart'
        }
    
    async def get_crypto_prices(self, symbols=['bitcoin', 'ethereum', 'apecoin']):
        """Get real-time cryptocurrency prices"""
        try:
            url = f"{self.base_urls['coingecko']}/simple/price"
            params = {
                'ids': ','.join(symbols),
                'vs_currencies': 'usd',
                'include_24hr_change': 'true',
                'include_market_cap': 'true'
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.format_crypto_data(data)
                    else:
                        return "Unable to fetch crypto prices at this time"
        except Exception as e:
            return f"Crypto price feed error: {str(e)}"
    
    def format_crypto_data(self, data):
        """Format cryptocurrency data for display"""
        formatted = "🪙 **Real-Time Crypto Prices:**\n\n"
        
        for coin, info in data.items():
            price = info.get('usd', 0)
            change_24h = info.get('usd_24h_change', 0)
            market_cap = info.get('usd_market_cap', 0)
            
            change_emoji = "📈" if change_24h > 0 else "📉"
            formatted += f"**{coin.title()}**: ${price:,.2f} {change_emoji} {change_24h:+.2f}%\n"
            formatted += f"Market Cap: ${market_cap:,.0f}\n\n"
        
        formatted += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*"
        return formatted
    
    async def get_stock_data(self, symbol='SPY'):
        """Get real-time stock market data"""
        try:
            url = f"{self.base_urls['yahoo_finance']}/{symbol}"
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.format_stock_data(data, symbol)
                    else:
                        return f"Unable to fetch stock data for {symbol}"
        except Exception as e:
            return f"Stock data feed error: {str(e)}"
    
    def format_stock_data(self, data, symbol):
        """Format stock data for display"""
        try:
            result = data['chart']['result'][0]
            meta = result['meta']
            
            current_price = meta.get('regularMarketPrice', 0)
            prev_close = meta.get('previousClose', 0)
            change = current_price - prev_close
            change_pct = (change / prev_close) * 100 if prev_close else 0
            
            change_emoji = "📈" if change > 0 else "📉"
            
            formatted = f"📊 **{symbol} Stock Data:**\n\n"
            formatted += f"**Current Price**: ${current_price:.2f} {change_emoji} {change:+.2f} ({change_pct:+.2f}%)\n"
            formatted += f"**Previous Close**: ${prev_close:.2f}\n"
            formatted += f"**Market**: {meta.get('exchangeName', 'N/A')}\n\n"
            formatted += f"*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*"
            
            return formatted
        except Exception as e:
            return f"Error formatting stock data: {str(e)}"
    
    async def get_news_sentiment(self, query='cryptocurrency market'):
        """Get news sentiment analysis"""
        try:
            url = f"{self.base_urls['news_api']}/everything"
            params = {
                'q': query,
                'sortBy': 'publishedAt',
                'pageSize': 5,
                'apiKey': self.api_keys['news_api']
            }
            
            async with aiohttp.ClientSession() as session:
                async with session.get(url, params=params) as response:
                    if response.status == 200:
                        data = await response.json()
                        return self.analyze_news_sentiment(data['articles'])
                    else:
                        return "Unable to fetch news data"
        except Exception as e:
            return f"News sentiment error: {str(e)}"
    
    def analyze_news_sentiment(self, articles):
        """Analyze sentiment from news articles"""
        if not articles:
            return "No recent news articles found"
        
        sentiment_analysis = "📰 **News Sentiment Analysis:**\n\n"
        
        positive_words = ['surge', 'bullish', 'gains', 'positive', 'growth', 'rally']
        negative_words = ['crash', 'bearish', 'losses', 'negative', 'decline', 'fall']
        
        sentiment_scores = []
        
        for article in articles[:3]:
            title = article.get('title', '')
            description = article.get('description', '')
            text = f"{title} {description}".lower()
            
            pos_count = sum(1 for word in positive_words if word in text)
            neg_count = sum(1 for word in negative_words if word in text)
            
            if pos_count > neg_count:
                sentiment = "Positive 📈"
                score = 1
            elif neg_count > pos_count:
                sentiment = "Negative 📉"
                score = -1
            else:
                sentiment = "Neutral ➡️"
                score = 0
            
            sentiment_scores.append(score)
            sentiment_analysis += f"**{title[:60]}...**: {sentiment}\n"
        
        # Overall sentiment
        avg_sentiment = sum(sentiment_scores) / len(sentiment_scores) if sentiment_scores else 0
        if avg_sentiment > 0.2:
            overall = "Overall Positive 📈"
        elif avg_sentiment < -0.2:
            overall = "Overall Negative 📉"
        else:
            overall = "Overall Neutral ➡️"
        
        sentiment_analysis += f"\n**{overall}**"
        return sentiment_analysis
    
    async def get_economic_indicators(self):
        """Get key economic indicators"""
        try:
            # Simplified economic data (would use real APIs in production)
            indicators = {
                'VIX': {'value': 18.5, 'change': -2.1, 'description': 'Market Volatility'},
                'DXY': {'value': 103.2, 'change': 0.3, 'description': 'US Dollar Index'},
                'GOLD': {'value': 2045.0, 'change': 12.5, 'description': 'Gold Price (USD/oz)'},
                'OIL': {'value': 78.2, 'change': -1.8, 'description': 'Crude Oil (WTI)'}
            }
            
            formatted = "📊 **Economic Indicators:**\n\n"
            
            for symbol, data in indicators.items():
                change_emoji = "📈" if data['change'] > 0 else "📉"
                formatted += f"**{symbol}** ({data['description']}): {data['value']} {change_emoji} {data['change']:+.1f}\n"
            
            formatted += f"\n*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}*"
            return formatted
            
        except Exception as e:
            return f"Economic indicators error: {str(e)}"

# Global instance
data_feeds = RealTimeDataFeeds()

async def get_crypto_market_data(symbols=None):
    """Get cryptocurrency market data"""
    if symbols is None:
        symbols = ['bitcoin', 'ethereum', 'apecoin']
    return await data_feeds.get_crypto_prices(symbols)

async def get_stock_market_data(symbol='SPY'):
    """Get stock market data"""
    return await data_feeds.get_stock_data(symbol)

async def get_market_sentiment(query='cryptocurrency'):
    """Get market sentiment from news"""
    return await data_feeds.get_news_sentiment(f"{query} market")

async def get_economic_data():
    """Get economic indicators"""
    return await data_feeds.get_economic_indicators()