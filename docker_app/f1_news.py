#!/usr/bin/env python3
"""
Module for fetching F1 news from ESPN and other sources
"""

import requests
import json
from datetime import datetime

ESPN_F1_API = "https://site.api.espn.com/apis/site/v2/sports/racing/f1"

def get_f1_news(limit=5):
    """Get the latest F1 news from ESPN"""
    try:
        url = f"{ESPN_F1_API}/news"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return "F1 news currently unavailable. Please check Formula1.com for the latest news."
            
        data = response.json()
        articles = data.get("articles", [])
        
        if not articles:
            return "No recent F1 news found. Please check Formula1.com for the latest news."
            
        # Format the news articles
        news_items = ["Latest F1 News:"]
        
        for i, article in enumerate(articles[:limit]):
            title = article.get("headline", "Unknown")
            description = article.get("description", "")
            published = article.get("published", "")
            
            # Format the date
            if published:
                try:
                    date_obj = datetime.fromisoformat(published.replace("Z", "+00:00"))
                    published = date_obj.strftime("%Y-%m-%d")
                except:
                    pass
                    
            news_items.append(f"{i+1}. {title} ({published})")
            if description:
                news_items.append(f"   {description[:150]}...")
                
        return "\n".join(news_items)
    except Exception as e:
        print(f"Error getting F1 news: {str(e)}")
        return "F1 news currently unavailable. Please check Formula1.com for the latest news."

def get_f1_scoreboard():
    """Get the current F1 scoreboard from ESPN"""
    try:
        url = f"{ESPN_F1_API}/scoreboard"
        response = requests.get(url, timeout=10)
        
        if response.status_code != 200:
            return None
            
        data = response.json()
        events = data.get("events", [])
        
        if not events:
            return None
            
        # Get the most recent/upcoming event
        event = events[0]
        name = event.get("name", "Unknown")
        date = event.get("date", "")
        status = event.get("status", {}).get("type", {}).get("description", "Scheduled")
        
        # Format the date
        if date:
            try:
                date_obj = datetime.fromisoformat(date.replace("Z", "+00:00"))
                date = date_obj.strftime("%Y-%m-%d %H:%M UTC")
            except:
                pass
                
        return f"Next F1 Event: {name} - {date} ({status})"
    except Exception as e:
        print(f"Error getting F1 scoreboard: {str(e)}")
        return None

if __name__ == "__main__":
    # Test the functions
    print(get_f1_news())
    print("\n" + "-"*50 + "\n")
    print(get_f1_scoreboard())