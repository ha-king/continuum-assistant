#!/usr/bin/env python3
"""
Test script for Formula 1 assistant's data integration capabilities
"""

from formula1_assistant import (
    get_current_session_info,
    get_driver_info,
    get_race_results,
    get_qualifying_results,
    get_f1_calendar,
    get_f1_standings,
    get_next_f1_race
)

try:
    from f1_news import get_f1_news, get_f1_scoreboard
    has_news_module = True
except ImportError:
    has_news_module = False

def test_f1_data_integration():
    print("Testing Formula 1 Data Integration\n" + "="*50)
    
    # Test OpenF1 API integration
    print("\n1. OpenF1 API Integration:")
    print("-" * 40)
    
    print("Current Session Info:")
    session_info = get_current_session_info()
    print(session_info if session_info else "No session info available")
    
    print("\nDriver Info:")
    driver_info = get_driver_info()
    print(driver_info if driver_info else "No driver info available")
    
    print("\nRace Results:")
    race_results = get_race_results()
    print(race_results if race_results else "No race results available")
    
    print("\nQualifying Results:")
    quali_results = get_qualifying_results()
    print(quali_results if quali_results else "No qualifying results available")
    
    print("\nF1 Calendar:")
    calendar = get_f1_calendar()
    print(calendar if calendar else "No calendar available")
    
    # Test Ergast API integration
    print("\n2. Ergast API Integration:")
    print("-" * 40)
    
    print("F1 Standings:")
    standings = get_f1_standings()
    print(standings if standings else "No standings available")
    
    print("\nNext Race Info:")
    next_race = get_next_f1_race()
    print(next_race if next_race else "No next race info available")
    
    # Test ESPN F1 API integration
    if has_news_module:
        print("\n3. ESPN F1 API Integration:")
        print("-" * 40)
        
        print("F1 News:")
        news = get_f1_news(limit=2)
        print(news if news else "No news available")
        
        print("\nF1 Scoreboard:")
        scoreboard = get_f1_scoreboard()
        print(scoreboard if scoreboard else "No scoreboard available")

if __name__ == "__main__":
    test_f1_data_integration()