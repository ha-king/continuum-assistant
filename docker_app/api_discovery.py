#!/usr/bin/env python3
"""
API Discovery for Real-Time Data Sources
Maps each assistant to required APIs and data sources
"""

API_MAPPING = {
    # Financial & Crypto Assistants
    "financial_assistant": {
        "primary": ["CoinGecko API", "Alpha Vantage", "Yahoo Finance"],
        "endpoints": [
            "https://api.coingecko.com/api/v3/simple/price",
            "https://query1.finance.yahoo.com/v8/finance/chart/",
            "https://www.alphavantage.co/query"
        ],
        "data_types": ["crypto_prices", "stock_prices", "forex", "market_data"]
    },
    
    "cryptocurrency_assistant": {
        "primary": ["CoinGecko API", "CoinMarketCap", "Binance API"],
        "endpoints": [
            "https://api.coingecko.com/api/v3/simple/price",
            "https://api.coinmarketcap.com/v1/ticker/",
            "https://api.binance.com/api/v3/ticker/price"
        ],
        "data_types": ["crypto_prices", "market_cap", "trading_volume", "defi_data"]
    },
    
    # Sports Assistants
    "formula1_assistant": {
        "primary": ["OpenF1 API", "ESPN F1", "Ergast API"],
        "endpoints": [
            "https://api.openf1.org/v1/sessions",
            "https://site.api.espn.com/apis/site/v2/sports/racing/f1/scoreboard",
            "https://ergast.com/api/f1/current/next.json"
        ],
        "data_types": ["race_schedule", "live_timing", "driver_standings", "lap_times"]
    },
    
    "sports_assistant": {
        "primary": ["ESPN API", "OpenF1 API", "Sports API"],
        "endpoints": [
            "https://site.api.espn.com/apis/site/v2/sports/",
            "https://api.openf1.org/v1/",
            "https://api.sportsdata.io/"
        ],
        "data_types": ["scores", "schedules", "standings", "player_stats"]
    },
    
    # Research & Web Assistants
    "research_assistant": {
        "primary": ["NewsAPI", "Reddit API", "Google Trends"],
        "endpoints": [
            "https://newsapi.org/v2/everything",
            "https://www.reddit.com/r/all/hot.json",
            "https://trends.google.com/trends/api/"
        ],
        "data_types": ["news", "trends", "social_media", "academic_papers"]
    },
    
    "web_browser_assistant": {
        "primary": ["Direct HTTP", "Wayback Machine", "PageSpeed API"],
        "endpoints": [
            "https://web.archive.org/cdx/search/cdx",
            "https://www.googleapis.com/pagespeedonline/v5/runPagespeed"
        ],
        "data_types": ["website_content", "seo_data", "performance_metrics"]
    },
    
    # Tech Assistants
    "aws_assistant": {
        "primary": ["AWS Status API", "AWS What's New RSS"],
        "endpoints": [
            "https://status.aws.amazon.com/rss/all.rss",
            "https://aws.amazon.com/about-aws/whats-new/recent/feed/"
        ],
        "data_types": ["service_status", "new_features", "pricing_updates"]
    },
    
    "ai_assistant": {
        "primary": ["Hugging Face API", "Papers With Code", "GitHub API"],
        "endpoints": [
            "https://huggingface.co/api/models",
            "https://paperswithcode.com/api/v1/",
            "https://api.github.com/search/repositories"
        ],
        "data_types": ["model_releases", "research_papers", "code_repositories"]
    },
    
    # Business Assistants
    "business_assistant": {
        "primary": ["SEC EDGAR", "Company APIs", "Economic Data APIs"],
        "endpoints": [
            "https://data.sec.gov/api/xbrl/companyconcept/",
            "https://api.census.gov/data/",
            "https://fred.stlouisfed.org/api/"
        ],
        "data_types": ["company_filings", "economic_indicators", "market_data"]
    },
    
    # Weather & Location
    "weather_queries": {
        "primary": ["OpenWeatherMap", "WeatherAPI", "NOAA"],
        "endpoints": [
            "https://api.openweathermap.org/data/2.5/weather",
            "https://api.weatherapi.com/v1/current.json",
            "https://api.weather.gov/"
        ],
        "data_types": ["current_weather", "forecasts", "alerts"]
    },
    
    # News & Current Events
    "news_queries": {
        "primary": ["NewsAPI", "Associated Press", "Reuters"],
        "endpoints": [
            "https://newsapi.org/v2/top-headlines",
            "https://api.ap.org/",
            "https://www.reuters.com/pf/api/"
        ],
        "data_types": ["breaking_news", "headlines", "articles"]
    }
}

def get_apis_for_assistant(assistant_name: str) -> dict:
    """Get API requirements for specific assistant"""
    return API_MAPPING.get(assistant_name, {})

def get_all_required_apis() -> set:
    """Get all unique APIs needed across assistants"""
    apis = set()
    for assistant_data in API_MAPPING.values():
        apis.update(assistant_data.get("primary", []))
    return apis

def print_api_summary():
    """Print summary of API requirements"""
    print("API Requirements by Assistant:")
    print("=" * 50)
    
    for assistant, data in API_MAPPING.items():
        print(f"\n{assistant}:")
        print(f"  APIs: {', '.join(data.get('primary', []))}")
        print(f"  Data: {', '.join(data.get('data_types', []))}")
    
    print(f"\nTotal unique APIs needed: {len(get_all_required_apis())}")
    print("Unique APIs:", sorted(get_all_required_apis()))

if __name__ == "__main__":
    print_api_summary()