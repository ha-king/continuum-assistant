#!/usr/bin/env python3
"""
Test script for Coinbase API integration
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from coinbase_api_service import CoinbaseAPIService, get_coinbase_price_data
from crypto_data_service import get_enhanced_crypto_data
from cryptocurrency_assistant import cryptocurrency_assistant

def test_coinbase_service():
    """Test the Coinbase API service directly"""
    print("=" * 60)
    print("TESTING COINBASE API SERVICE")
    print("=" * 60)
    
    service = CoinbaseAPIService()
    
    # Test 1: Spot price
    print("\n1. Testing spot price for BTC-USD:")
    btc_price = service.get_spot_price('BTC-USD')
    if btc_price:
        print(f"   ✓ BTC Price: ${btc_price['price']:,.2f}")
        print(f"   ✓ Timestamp: {btc_price['timestamp']}")
    else:
        print("   ✗ Failed to get BTC price")
    
    # Test 2: Multiple prices
    print("\n2. Testing multiple cryptocurrency prices:")
    symbols = ['BTC', 'ETH', 'SOL']
    prices = service.get_current_prices(symbols)
    for symbol, data in prices.items():
        if data:
            print(f"   ✓ {symbol}: ${data['price']:,.2f}")
        else:
            print(f"   ✗ {symbol}: Failed to get price")
    
    # Test 3: Price statistics
    print("\n3. Testing price statistics for ETH-USD:")
    eth_stats = service.get_price_stats('ETH-USD')
    if eth_stats:
        print(f"   ✓ ETH Stats: Last=${eth_stats.get('last', 'N/A')}")
        if 'high' in eth_stats:
            print(f"   ✓ 24h High: ${eth_stats['high']:,.2f}")
        if 'low' in eth_stats:
            print(f"   ✓ 24h Low: ${eth_stats['low']:,.2f}")
    else:
        print("   ✗ Failed to get ETH statistics")
    
    # Test 4: Historical data
    print("\n4. Testing historical data for BTC (7 days):")
    historical = service.get_historical_prices('BTC-USD', 7)
    if historical and len(historical) > 0:
        print(f"   ✓ Retrieved {len(historical)} historical data points")
        print(f"   ✓ Oldest: {historical[0]['date']} - ${historical[0]['price']:,.2f}")
        print(f"   ✓ Latest: {historical[-1]['date']} - ${historical[-1]['price']:,.2f}")
        
        # Calculate trend
        if len(historical) >= 2:
            start_price = historical[0]['price']
            end_price = historical[-1]['price']
            change = ((end_price - start_price) / start_price) * 100
            trend = "📈" if change > 0 else "📉"
            print(f"   ✓ 7-day trend: {trend} {change:+.2f}%")
    else:
        print("   ✗ Failed to get historical data")
    
    # Test 5: Formatted price data
    print("\n5. Testing formatted price data:")
    formatted_btc = service.format_price_data('BTC')
    formatted_eth = service.format_price_data('ETH')
    print(f"   ✓ BTC: {formatted_btc}")
    print(f"   ✓ ETH: {formatted_eth}")

def test_enhanced_crypto_data():
    """Test the enhanced crypto data service"""
    print("\n" + "=" * 60)
    print("TESTING ENHANCED CRYPTO DATA SERVICE")
    print("=" * 60)
    
    test_queries = [
        "What's the current price of Bitcoin?",
        "Compare Ethereum and Solana prices",
        "Show me Bitcoin trend for the past week",
        "What are the current crypto market conditions?"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        try:
            result = get_enhanced_crypto_data(query)
            print(f"   ✓ Result: {result}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")

def test_coinbase_price_data():
    """Test the Coinbase price data function"""
    print("\n" + "=" * 60)
    print("TESTING COINBASE PRICE DATA FUNCTION")
    print("=" * 60)
    
    test_queries = [
        "Bitcoin price",
        "ETH and SOL comparison",
        "BTC weekly trend",
        "Ethereum monthly performance"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        try:
            result = get_coinbase_price_data(query)
            print(f"   ✓ Result: {result}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")

def test_cryptocurrency_assistant():
    """Test the full cryptocurrency assistant"""
    print("\n" + "=" * 60)
    print("TESTING CRYPTOCURRENCY ASSISTANT")
    print("=" * 60)
    
    test_queries = [
        "What's the current Bitcoin price and how has it performed this week?",
        "Compare Ethereum and Solana - which is performing better?",
        "Give me a market analysis of the top cryptocurrencies"
    ]
    
    for i, query in enumerate(test_queries, 1):
        print(f"\n{i}. Query: {query}")
        print("-" * 40)
        try:
            result = cryptocurrency_assistant(query)
            print(f"Assistant Response:\n{result}")
        except Exception as e:
            print(f"   ✗ Error: {str(e)}")
        print("-" * 40)

def main():
    """Run all tests"""
    print("COINBASE API INTEGRATION TEST SUITE")
    print("=" * 60)
    
    try:
        # Test individual components
        test_coinbase_service()
        test_enhanced_crypto_data()
        test_coinbase_price_data()
        
        # Test full assistant integration
        test_cryptocurrency_assistant()
        
        print("\n" + "=" * 60)
        print("TEST SUITE COMPLETED")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nCRITICAL ERROR: {str(e)}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit_code = main()
    sys.exit(exit_code)