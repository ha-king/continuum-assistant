"""
Test Knowledge Integration
Tests the integration of shared knowledge across assistants
"""

import unittest
from shared_knowledge import store_knowledge, retrieve_knowledge, learn_from_interaction
from aircraft_registry import get_registration
from aircraft_learning import get_learned_registration
from aviation_data_access import aviation_data

class TestKnowledgeIntegration(unittest.TestCase):
    """Test knowledge integration across assistants"""
    
    def test_knowledge_storage_retrieval(self):
        """Test basic knowledge storage and retrieval"""
        # Store test knowledge
        test_data = "N628TS is a Gulfstream G650ER"
        store_knowledge("elonjet", test_data, "test")
        
        # Retrieve test knowledge
        result = retrieve_knowledge("elonjet")
        self.assertIsNotNone(result)
        self.assertEqual(result.get("data"), test_data)
        
        # Test retrieval with different case
        result = retrieve_knowledge("ElonJet")
        self.assertIsNotNone(result)
        self.assertEqual(result.get("data"), test_data)
    
    def test_learning_from_interaction(self):
        """Test learning from interactions"""
        # Simulate interaction
        query = "Where is ElonJet now?"
        response = "ElonJet (registration N628TS) is currently on the ground at KLAX."
        
        # Learn from interaction
        learn_from_interaction(query, response)
        
        # Test if knowledge was stored
        result = retrieve_knowledge("elonjet")
        self.assertIsNotNone(result)
        
        # Test if we can extract registration
        import re
        reg_matches = re.findall(r'[N][0-9]{1,5}[A-Z]{0,2}', result.get("data", ""))
        self.assertTrue(len(reg_matches) > 0)
        self.assertEqual(reg_matches[0], "N628TS")
    
    def test_aviation_data_integration(self):
        """Test aviation data integration with knowledge base"""
        # Store test knowledge
        test_data = "ElonJet uses registration N628TS"
        store_knowledge("elonjet", test_data, "test")
        
        # Test aviation data enhancement
        enhanced = aviation_data.enhance_aviation_query("Where is ElonJet now?")
        
        # Check if enhancement contains flight position
        self.assertIn("FLIGHT POSITION", enhanced)
    
    def test_aircraft_registry_integration(self):
        """Test aircraft registry integration with knowledge base"""
        # Store test knowledge
        test_data = "ElonJet registration is N628TS"
        store_knowledge("elonjet", test_data, "test")
        
        # Test registration lookup
        reg = get_registration("elonjet")
        self.assertIsNotNone(reg)
        self.assertEqual(reg, "N628TS")

if __name__ == "__main__":
    unittest.main()