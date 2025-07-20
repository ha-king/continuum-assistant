"""
Aircraft Learning System
Learns and stores aircraft information from queries and responses
"""

import re
from typing import Optional, Dict
from datetime import datetime

class AircraftLearningSystem:
    """System that learns aircraft information from queries and responses"""
    
    def __init__(self):
        self.learned_data = {}
        
    def extract_and_store(self, query: str, response: str) -> None:
        """Extract aircraft information from query-response pairs and store it"""
        try:
            # Extract aircraft identifiers from query
            aircraft_names = self._extract_aircraft_names(query)
            
            # Extract registration numbers from response
            registrations = self._extract_registrations(response)
            
            # If we found both names and registrations, store the associations
            if aircraft_names and registrations:
                for name in aircraft_names:
                    for reg in registrations:
                        self._store_association(name, reg)
        except:
            pass
    
    def _extract_aircraft_names(self, text: str) -> list:
        """Extract potential aircraft names from text"""
        names = []
        text_lower = text.lower()
        
        # Look for common patterns
        patterns = [
            r'([a-z]+)\s*jet',
            r'([a-z]+)\s*aircraft',
            r'([a-z]+)\s*plane',
            r'([a-z]+)\'s\s*jet'
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, text_lower)
            names.extend(matches)
        
        # Also check for specific keywords
        keywords = ['elonjet', 'airforce one', 'air force one']
        for keyword in keywords:
            if keyword in text_lower:
                names.append(keyword)
        
        return names
    
    def _extract_registrations(self, text: str) -> list:
        """Extract aircraft registration numbers from text"""
        # Look for N-numbers (US registrations)
        n_numbers = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', text)
        
        # Look for other registration formats (international)
        other_regs = re.findall(r'[A-Z]{1,2}-[A-Z0-9]{1,5}', text)
        
        return n_numbers + other_regs
    
    def _store_association(self, name: str, registration: str) -> None:
        """Store association between aircraft name and registration"""
        try:
            # In a real implementation, this would store to a persistent knowledge base
            from strands import Agent
            from strands_tools import memory, use_llm
            
            # Create agent with memory access
            agent = Agent(tools=[memory, use_llm])
            
            # Store the association in the knowledge base
            agent.tool.memory(
                action="store",
                content=f"Aircraft '{name}' has registration number {registration}. Last updated: {datetime.now().isoformat()}"
            )
            
            # Also store in local cache
            self.learned_data[name] = registration
        except:
            # Fall back to local storage if knowledge base isn't available
            self.learned_data[name] = registration
    
    def get_registration(self, name: str) -> Optional[str]:
        """Get registration for an aircraft by name"""
        name_lower = name.lower()
        
        # Check local cache first
        if name_lower in self.learned_data:
            return self.learned_data[name_lower]
        
        # Then try knowledge base
        try:
            from strands import Agent
            from strands_tools import memory, use_llm
            
            # Create agent with memory access
            agent = Agent(tools=[memory, use_llm])
            
            # Query the knowledge base
            kb_results = agent.tool.memory(
                action="retrieve",
                query=f"aircraft registration for {name_lower}",
                min_score=0.7,
                max_results=1
            )
            
            # Extract registration from results if found
            if kb_results:
                # Parse the result to find N-number pattern
                matches = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', str(kb_results))
                if matches:
                    # Cache the result
                    self.learned_data[name_lower] = matches[0]
                    return matches[0]
        except:
            pass
        
        return None

# Global instance
aircraft_learning = AircraftLearningSystem()

def learn_from_interaction(query: str, response: str) -> None:
    """Learn aircraft information from query-response pairs"""
    aircraft_learning.extract_and_store(query, response)

def get_learned_registration(name: str) -> Optional[str]:
    """Get learned registration for an aircraft"""
    return aircraft_learning.get_registration(name)