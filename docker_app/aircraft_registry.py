"""
Aircraft Registry Lookup System
Provides dynamic lookup for aircraft by owner, nickname, or other identifiers
"""

import requests
import re
import json
from typing import Optional, Dict, List, Tuple
from datetime import datetime

class AircraftRegistry:
    """Dynamic aircraft registry lookup system"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 10
        self.cache = {}
        self.cache_time = {}
        self.cache_duration = 3600  # 1 hour
        
        # Initialize aircraft registry
        self._init_aircraft_registry()
    
    def _init_aircraft_registry(self):
        """Initialize aircraft registry from external sources"""
        try:
            # Try to load from external source
            url = "https://raw.githubusercontent.com/aircraft-data/registry/main/high-profile.json"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                for entry in data:
                    name = entry.get('name', '').lower()
                    reg = entry.get('registration')
                    if name and reg:
                        self.cache[name] = reg
                        self.cache_time[name] = datetime.now().timestamp()
        except:
            # Use a generic aircraft registry lookup service
            self._load_from_registry_service()
    
    def _load_from_registry_service(self):
        """Load aircraft data from registry service"""
        # This would connect to a real aircraft registry service
        # For now, we'll rely on the dynamic lookup methods
        pass
    
    def lookup_by_name(self, name: str) -> Optional[str]:
        """Look up aircraft registration by name/owner/nickname"""
        name_lower = name.lower()
        
        # Check cache first
        if name_lower in self.cache:
            # Check if cache is still valid
            if datetime.now().timestamp() - self.cache_time.get(name_lower, 0) < self.cache_duration:
                return self.cache[name_lower]
        
        # Try to find registration using various methods
        registration = self._search_registry_apis(name_lower)
        
        if registration:
            # Cache the result
            self.cache[name_lower] = registration
            self.cache_time[name_lower] = datetime.now().timestamp()
            return registration
        
        return None
    
    def _search_registry_apis(self, query: str) -> Optional[str]:
        """Search multiple registry APIs for aircraft"""
        # Try public aircraft registry APIs
        try:
            # First try the FAA registry API
            url = f"https://registry.faa.gov/api/aircraft/search?q={query}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'results' in data and data['results']:
                    # Return the first match
                    return data['results'][0].get('registration')
        except:
            pass
        
        # Try alternative sources
        sources = [
            self._search_jetphotos,
            self._search_flightaware,
            self._search_planespotters,
            self._search_adsbexchange
        ]
        
        for source in sources:
            try:
                result = source(query)
                if result:
                    return result
            except:
                continue
        
        return None
    
    def _search_jetphotos(self, query: str) -> Optional[str]:
        """Search JetPhotos for aircraft"""
        try:
            url = f"https://www.jetphotos.com/api/v1/search?keyword={query}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'results' in data and data['results']:
                    # Extract registration from results
                    for result in data['results']:
                        if 'registration' in result:
                            return result['registration']
        except:
            pass
        
        return None
    
    def _search_flightaware(self, query: str) -> Optional[str]:
        """Search FlightAware for aircraft"""
        try:
            # This is a simplified approach - real implementation would use their API
            url = f"https://flightaware.com/live/fleet/{query}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                # Look for registration patterns in the HTML
                content = response.text
                # Look for N-number pattern
                matches = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', content)
                if matches:
                    return matches[0]
        except:
            pass
        
        return None
    
    def _search_planespotters(self, query: str) -> Optional[str]:
        """Search Planespotters for aircraft"""
        try:
            url = f"https://api.planespotters.net/pub/photos/search?query={query}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                data = response.json()
                if data and 'photos' in data and data['photos']:
                    # Extract registration from photos
                    for photo in data['photos']:
                        if 'registration' in photo:
                            return photo['registration']
        except:
            pass
        
        return None
    
    def _search_adsbexchange(self, query: str) -> Optional[str]:
        """Search ADS-B Exchange for aircraft"""
        try:
            # Use ADS-B Exchange API to search for aircraft
            # This would be a real API call in production
            url = f"https://adsbexchange-api.example.com/v2/registration/{query}"
            
            # In a real implementation, this would make an actual API call
            # For now, we'll use the knowledge base lookup instead
            return self._search_knowledge_base(query)
        except:
            pass
        
        return None
        
    def _search_knowledge_base(self, query: str) -> Optional[str]:
        """Search knowledge base for aircraft information"""
        try:
            # In a real implementation, this would query a knowledge base
            # that stores previously discovered aircraft information
            from strands import Agent
            from strands_tools import memory, use_llm
            
            # Create agent with memory access
            agent = Agent(tools=[memory, use_llm])
            
            # Query the knowledge base
            kb_results = agent.tool.memory(
                action="retrieve",
                query=f"aircraft registration for {query}",
                min_score=0.7,
                max_results=1
            )
            
            # Extract registration from results if found
            if kb_results:
                # Parse the result to find N-number pattern
                import re
                matches = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', str(kb_results))
                if matches:
                    return matches[0]
        except:
            pass
            
        return None
    
    def get_registration_by_nickname(self, nickname: str) -> Optional[str]:
        """Get aircraft registration by nickname or common name"""
        nickname_lower = nickname.lower()
        
        # Check for direct matches in cache first
        if nickname_lower in self.cache:
            return self.cache[nickname_lower]
            
        # Check for partial matches in cache
        for cached_name in self.cache.keys():
            if cached_name in nickname_lower or nickname_lower in cached_name:
                return self.cache[cached_name]
        
        # Try to find in registry
        return self.lookup_by_name(nickname_lower)

# Global instance
aircraft_registry = AircraftRegistry()

def get_registration(name_or_nickname: str) -> Optional[str]:
    """Convenience function to get registration by name or nickname"""
    return aircraft_registry.get_registration_by_nickname(name_or_nickname)