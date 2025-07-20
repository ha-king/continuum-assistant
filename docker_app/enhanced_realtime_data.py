"""
Enhanced Real-Time Data Access with ESPN and OpenF1 APIs
"""

import requests
import json
from datetime import datetime
from typing import Optional

class EnhancedRealTimeData:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 10

    def get_f1_data_espn(self) -> Optional[str]:
        """Get F1 data from ESPN API"""
        try:
            url = "https://site.api.espn.com/apis/site/v2/sports/racing/f1/scoreboard"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                events = data.get('events', [])
                if events:
                    event = events[0]
                    name = event.get('name', 'Unknown')
                    date = event.get('date', 'TBD')
                    status = event.get('status', {}).get('type', {}).get('description', 'Scheduled')
                    return f"ESPN: {name} - {date} ({status})"
        except:
            pass
        return None

    def get_f1_data_openf1(self) -> Optional[str]:
        """Get F1 data from OpenF1 API"""
        try:
            # Get current sessions
            url = "https://api.openf1.org/v1/sessions?session_name=Race&year=2025"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                sessions = response.json()
                if sessions:
                    # Find next upcoming session
                    current_time = datetime.now()
                    for session in sessions:
                        session_date = session.get('date_start', '')
                        if session_date:
                            try:
                                session_dt = datetime.fromisoformat(session_date.replace('Z', '+00:00'))
                                if session_dt > current_time:
                                    location = session.get('location', 'Unknown')
                                    return f"OpenF1: Next race at {location} on {session_date[:10]}"
                            except:
                                continue
        except:
            pass
        return None

    def get_comprehensive_f1_data(self) -> str:
        """Get F1 data from multiple sources"""
        sources = []
        
        # Try ESPN
        espn_data = self.get_f1_data_espn()
        if espn_data:
            sources.append(espn_data)
        
        # Try OpenF1
        openf1_data = self.get_f1_data_openf1()
        if openf1_data:
            sources.append(openf1_data)
        
        # Try Ergast as fallback
        try:
            url = "https://ergast.com/api/f1/current/next.json"
            response = self.session.get(url, timeout=self.timeout)
            if response.status_code == 200:
                data = response.json()
                races = data.get('MRData', {}).get('RaceTable', {}).get('Races', [])
                if races:
                    race = races[0]
                    name = race.get('raceName', 'Unknown')
                    circuit = race.get('Circuit', {}).get('circuitName', 'Unknown')
                    date = race.get('date', 'TBD')
                    sources.append(f"Ergast: {name} at {circuit} on {date}")
        except:
            pass
        
        if sources:
            return " | ".join(sources)
        
        # Final fallback with seasonal context
        current_year = datetime.now().year
        current_month = datetime.now().month
        
        if current_month <= 2:
            return f"F1 {current_year} season starts March with pre-season testing"
        elif current_month >= 12:
            return f"F1 {current_year} season ending. Next season starts March {current_year + 1}"
        else:
            return f"F1 {current_year} season active. Check Formula1.com for live updates"

# Test the enhanced F1 data
if __name__ == "__main__":
    enhanced = EnhancedRealTimeData()
    result = enhanced.get_comprehensive_f1_data()
    print("Enhanced F1 Data:", result)