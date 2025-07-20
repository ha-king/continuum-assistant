"""
Aviation Knowledge Base
Provides general aviation information beyond live flight data
"""

from typing import Dict, List, Optional

class AviationKnowledge:
    """Aviation knowledge base for general aviation questions"""
    
    def __init__(self):
        self.aircraft_types = {
            "commercial": [
                "Boeing 737", "Boeing 747", "Boeing 777", "Boeing 787",
                "Airbus A320", "Airbus A330", "Airbus A350", "Airbus A380",
                "Embraer E-Jet", "Bombardier CRJ"
            ],
            "private": [
                "Cessna 172", "Cessna 182", "Piper PA-28", "Cirrus SR22",
                "Beechcraft Bonanza", "Diamond DA40", "Mooney M20"
            ],
            "business": [
                "Gulfstream G650", "Bombardier Global 7500", "Dassault Falcon",
                "Cessna Citation", "Embraer Phenom", "Pilatus PC-24"
            ]
        }
        
        self.airport_info = {
            "ATL": {"name": "Hartsfield-Jackson Atlanta International", "location": "Atlanta, GA", "runways": 5},
            "LAX": {"name": "Los Angeles International", "location": "Los Angeles, CA", "runways": 4},
            "ORD": {"name": "O'Hare International", "location": "Chicago, IL", "runways": 8},
            "DFW": {"name": "Dallas/Fort Worth International", "location": "Dallas-Fort Worth, TX", "runways": 7},
            "DEN": {"name": "Denver International", "location": "Denver, CO", "runways": 6},
            "JFK": {"name": "John F. Kennedy International", "location": "New York, NY", "runways": 4},
            "SFO": {"name": "San Francisco International", "location": "San Francisco, CA", "runways": 4}
        }
        
        self.faa_regulations = {
            "VFR": "Visual Flight Rules - Minimum visibility of 3 statute miles and cloud clearance requirements",
            "IFR": "Instrument Flight Rules - Used when weather conditions are below VFR minimums",
            "Part 91": "General Operating and Flight Rules for non-commercial operations",
            "Part 121": "Operating Requirements for Domestic, Flag, and Supplemental Air Carriers",
            "Part 135": "Operating Requirements for Commuter and On Demand Operations",
            "Part 61": "Certification for pilots, flight instructors, and ground instructors"
        }
        
        self.weather_codes = {
            "METAR": "Meteorological Aerodrome Report - Current weather observation",
            "TAF": "Terminal Aerodrome Forecast - Airport weather forecast",
            "SIGMET": "Significant Meteorological Information - Warnings about hazardous weather",
            "AIRMET": "Airmen's Meteorological Information - Advisories of significant weather"
        }
    
    def get_aircraft_info(self, aircraft_type: str) -> Optional[str]:
        """Get information about aircraft types"""
        aircraft_type = aircraft_type.lower()
        
        for category, aircraft_list in self.aircraft_types.items():
            for aircraft in aircraft_list:
                if aircraft_type in aircraft.lower():
                    return f"{aircraft} - {category.capitalize()} aircraft"
        
        return None
    
    def get_airport_info(self, airport_code: str) -> Optional[Dict]:
        """Get information about an airport by code"""
        airport_code = airport_code.upper()
        return self.airport_info.get(airport_code)
    
    def get_regulation_info(self, regulation: str) -> Optional[str]:
        """Get information about FAA regulations"""
        regulation = regulation.upper()
        return self.faa_regulations.get(regulation)
    
    def get_weather_code_info(self, code: str) -> Optional[str]:
        """Get information about aviation weather codes"""
        code = code.upper()
        return self.weather_codes.get(code)
    
    def enhance_aviation_query(self, query: str) -> str:
        """Add aviation knowledge to queries"""
        query_lower = query.lower()
        enhancements = []
        
        # Check for aircraft nicknames/special aircraft
        from aircraft_registry import get_registration
        
        # Look for keywords that might indicate special aircraft
        special_keywords = ['jet', 'aircraft', 'plane', 'elonjet', 'elon']
        if any(keyword in query_lower for keyword in special_keywords):
            # Extract potential names (2-3 word phrases)
            words = query_lower.split()
            for i in range(len(words)):
                # Try single word
                potential_name = words[i]
                reg = get_registration(potential_name)
                
                # Try two word phrase
                if i < len(words) - 1:
                    potential_name = f"{words[i]} {words[i+1]}"
                    reg = get_registration(potential_name) or reg
                
                # Try three word phrase
                if i < len(words) - 2:
                    potential_name = f"{words[i]} {words[i+1]} {words[i+2]}"
                    reg = get_registration(potential_name) or reg
                
                if reg:
                    enhancements.append(f"SPECIAL AIRCRAFT: Registration {reg} found for query terms")
                    break
        
        # Check for aircraft types
        for category, aircraft_list in self.aircraft_types.items():
            for aircraft in aircraft_list:
                if aircraft.lower() in query_lower:
                    enhancements.append(f"AIRCRAFT INFO: {aircraft} - {category.capitalize()} aircraft")
                    break
        
        # Check for airport codes
        for code, info in self.airport_info.items():
            if code.lower() in query_lower:
                enhancements.append(f"AIRPORT INFO: {code} - {info['name']} in {info['location']} with {info['runways']} runways")
                break
        
        # Check for regulations
        for reg, desc in self.faa_regulations.items():
            if reg.lower() in query_lower:
                enhancements.append(f"FAA REGULATION: {reg} - {desc}")
                break
        
        # Check for weather codes
        for code, desc in self.weather_codes.items():
            if code.lower() in query_lower:
                enhancements.append(f"WEATHER CODE: {code} - {desc}")
                break
        
        return "\n\n".join(enhancements)

# Global instance
aviation_knowledge = AviationKnowledge()

def enhance_with_aviation_knowledge(query: str) -> str:
    """Convenience function to enhance queries with aviation knowledge"""
    return aviation_knowledge.enhance_aviation_query(query)