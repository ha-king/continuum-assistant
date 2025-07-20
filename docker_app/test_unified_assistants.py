"""
Test script for unified assistants and router
"""

import unittest
from unittest.mock import patch, MagicMock
from unified_assistants import (
    business_finance_assistant,
    tech_security_assistant,
    research_knowledge_assistant,
    specialized_industries_assistant,
    universal_assistant,
    detect_domain
)
from unified_router import unified_route

class TestUnifiedAssistants(unittest.TestCase):
    
    def test_domain_detection(self):
        """Test that domain detection correctly identifies query domains"""
        # Business & Finance queries
        self.assertEqual(detect_domain("What's the current price of Bitcoin?"), "business_finance")
        self.assertEqual(detect_domain("How do I create a business plan?"), "business_finance")
        self.assertEqual(detect_domain("Explain stock market trends"), "business_finance")
        
        # Technology & Security queries
        self.assertEqual(detect_domain("How do I secure my AWS account?"), "tech_security")
        self.assertEqual(detect_domain("Write a Python function to sort a list"), "tech_security")
        self.assertEqual(detect_domain("What are the latest cybersecurity threats?"), "tech_security")
        
        # Research & Knowledge queries
        self.assertEqual(detect_domain("Research the history of quantum computing"), "research_knowledge")
        self.assertEqual(detect_domain("Calculate the area of a circle with radius 5"), "research_knowledge")
        self.assertEqual(detect_domain("Help me write an essay about climate change"), "research_knowledge")
        
        # Specialized Industries queries
        self.assertEqual(detect_domain("What's the status of flight UA123?"), "specialized_industries")
        self.assertEqual(detect_domain("Who won the last Formula 1 race?"), "specialized_industries")
        self.assertEqual(detect_domain("Explain Louisiana business law"), "specialized_industries")
        
        # Default to universal
        self.assertEqual(detect_domain("Tell me a joke"), "universal")
        self.assertEqual(detect_domain("What's the meaning of life?"), "universal")

    @patch('unified_router.track_router_decision')
    def test_unified_routing(self, mock_track):
        """Test that unified routing correctly routes queries to assistants"""
        # Mock assistants
        mock_assistants = {
            'business_finance': MagicMock(return_value="Business finance response"),
            'tech_security': MagicMock(return_value="Tech security response"),
            'research_knowledge': MagicMock(return_value="Research knowledge response"),
            'specialized_industries': MagicMock(return_value="Specialized industries response"),
            'universal': MagicMock(return_value="Universal response"),
            'aviation': MagicMock(return_value="Aviation response"),
            'formula1': MagicMock(return_value="Formula 1 response")
        }
        
        # Test time query
        assistant_func, enhanced_prompt = unified_route("What time is it?", "2023-06-15 10:30:00", mock_assistants)
        self.assertIsNone(assistant_func)
        self.assertTrue(enhanced_prompt.startswith("It is"))
        
        # Test aviation query
        assistant_func, enhanced_prompt = unified_route("What's the status of N12345?", "2023-06-15 10:30:00", mock_assistants)
        self.assertEqual(assistant_func, mock_assistants['aviation'])
        
        # Test formula1 query
        assistant_func, enhanced_prompt = unified_route("Who won the last Formula 1 race?", "2023-06-15 10:30:00", mock_assistants)
        self.assertEqual(assistant_func, mock_assistants['formula1'])
        
        # Test prediction query
        assistant_func, enhanced_prompt = unified_route("Predict the stock market next week", "2023-06-15 10:30:00", mock_assistants)
        self.assertEqual(assistant_func, mock_assistants['universal'])
        self.assertTrue("PREDICTION QUERY" in enhanced_prompt)

if __name__ == '__main__':
    unittest.main()