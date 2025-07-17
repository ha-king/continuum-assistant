"""
Aircraft Web Search Module
Searches the web for aircraft information based on registration or name
"""

import requests
import re
from typing import Optional, Dict, List
from bs4 import BeautifulSoup

class AircraftWebSearch:
    """Search the web for aircraft information"""
    
    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        self.timeout = 10
    
    def search_by_registration(self, registration: str) -> Dict:
        """Search for aircraft information by registration number"""
        results = {}
        
        # Try multiple sources
        sources = [
            self._search_flightaware,
            self._search_jetphotos,
            self._search_planespotters,
            self._search_faa
        ]
        
        for source in sources:
            try:
                source_results = source(registration)
                if source_results:
                    results.update(source_results)
            except Exception as e:
                continue
        
        return results
    
    def _search_flightaware(self, registration: str) -> Dict:
        """Search FlightAware for aircraft info"""
        results = {}
        try:
            url = f"https://flightaware.com/resources/registration/{registration}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract aircraft type
                type_elem = soup.select_one('.aircraftInfoValue')
                if type_elem:
                    results['aircraft_type'] = type_elem.text.strip()
                
                # Extract owner info
                owner_elem = soup.select_one('.ownerInfoValue')
                if owner_elem:
                    results['owner'] = owner_elem.text.strip()
                
                results['source'] = 'FlightAware'
                results['url'] = url
        except:
            pass
        
        return results
    
    def _search_jetphotos(self, registration: str) -> Dict:
        """Search JetPhotos for aircraft info"""
        results = {}
        try:
            url = f"https://www.jetphotos.com/registration/{registration}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract aircraft info
                info_elem = soup.select_one('.result__infoListText')
                if info_elem:
                    results['aircraft_info'] = info_elem.text.strip()
                
                # Extract image if available
                img_elem = soup.select_one('.result__photo img')
                if img_elem and 'src' in img_elem.attrs:
                    results['image_url'] = img_elem['src']
                
                results['source'] = 'JetPhotos'
                results['url'] = url
        except:
            pass
        
        return results
    
    def _search_planespotters(self, registration: str) -> Dict:
        """Search Planespotters for aircraft info"""
        results = {}
        try:
            url = f"https://www.planespotters.net/hex/{registration}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract aircraft info
                info_elems = soup.select('.table-striped td')
                if len(info_elems) >= 2:
                    results['aircraft_type'] = info_elems[1].text.strip()
                
                results['source'] = 'Planespotters'
                results['url'] = url
        except:
            pass
        
        return results
    
    def _search_faa(self, registration: str) -> Dict:
        """Search FAA registry for aircraft info"""
        results = {}
        try:
            # FAA registry lookup
            url = f"https://registry.faa.gov/AircraftInquiry/Search/NNumberResult?nNumberTxt={registration}"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract aircraft info
                info_table = soup.select('.table-striped tr')
                for row in info_table:
                    cells = row.select('td')
                    if len(cells) >= 2:
                        key = cells[0].text.strip().lower().replace(' ', '_')
                        value = cells[1].text.strip()
                        results[key] = value
                
                results['source'] = 'FAA Registry'
                results['url'] = url
        except:
            pass
        
        return results
    
    def search_by_name(self, name: str) -> Dict:
        """Search for aircraft information by name or nickname"""
        results = {}
        
        # First try to get registration
        from aircraft_registry import get_registration
        registration = get_registration(name)
        
        if registration:
            # If we found a registration, search by that
            return self.search_by_registration(registration)
        
        # Otherwise search directly by name
        try:
            # General web search
            url = f"https://duckduckgo.com/html/?q={name}+aircraft+registration"
            response = self.session.get(url, timeout=self.timeout)
            
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Extract search results
                results_elem = soup.select('.result__snippet')
                if results_elem:
                    snippets = [elem.text.strip() for elem in results_elem[:3]]
                    results['search_results'] = snippets
                
                # Look for N-numbers in results
                n_numbers = []
                for snippet in snippets:
                    matches = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', snippet)
                    n_numbers.extend(matches)
                
                if n_numbers:
                    results['possible_registrations'] = list(set(n_numbers))
                
                results['source'] = 'Web Search'
                results['url'] = url
        except:
            pass
        
        return results

# Global instance
aircraft_web_search = AircraftWebSearch()

def search_aircraft(identifier: str) -> Dict:
    """Search for aircraft by registration or name"""
    # Check if it looks like a registration (N-number)
    if identifier.upper().startswith('N') and len(identifier) >= 4:
        return aircraft_web_search.search_by_registration(identifier)
    else:
        return aircraft_web_search.search_by_name(identifier)