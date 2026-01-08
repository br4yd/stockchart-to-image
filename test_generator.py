#!/usr/bin/env python3

"""
Test script for stock chart generator.
Demonstrates usage and validates functionality.
"""

from stock_chart_generator import StockChartGenerator


def test_basic_generation():
    """Test basic chart generation with common tickers."""
    generator = StockChartGenerator()

    test_tickers = ['AAPL', 'MSFT', 'TSLA']

    print("Stock Chart Generator - Test Suite")
    print("=" * 50)

    for ticker in test_tickers:
        print(f"\nTesting {ticker}...")
        try:
            filepath = generator.generate(ticker)
            print(f"  Success: {filepath}")
        except Exception as e:
            print(f"  Failed: {str(e)}")

    print("\n" + "=" * 50)
    print("Test suite completed")


def test_data_fetch():
    """Test data fetching capability."""
    generator = StockChartGenerator()

    print("\nData Fetch Test")
    print("-" * 50)

    ticker = 'AAPL'
    data = generator.fetch_stock_data(ticker)

    if data is not None:
        print(f"Successfully fetched {len(data)} days of data for {ticker}")
        print(f"\nData preview:")
        print(data[['date', 'close']].to_string())
    else:
        print(f"Failed to fetch data for {ticker}")


def test_invalid_ticker():
    """Test handling of invalid ticker."""
    generator = StockChartGenerator()

    print("\n\nInvalid Ticker Test")
    print("-" * 50)

    invalid_ticker = 'INVALIDTICKER123'
    data = generator.fetch_stock_data(invalid_ticker)

    if data is None:
        print(f"Correctly handled invalid ticker: {invalid_ticker}")
    else:
        print(f"Unexpected: Got data for invalid ticker")


if __name__ == "__main__":
    print("Choose test to run:")
    print("1. Basic generation test (generates charts for AAPL, MSFT, TSLA)")
    print("2. Data fetch test (displays raw data)")
    print("3. Invalid ticker test")
    print("4. Run all tests")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == '1':
        test_basic_generation()
    elif choice == '2':
        test_data_fetch()
    elif choice == '3':
        test_invalid_ticker()
    elif choice == '4':
        test_data_fetch()
        test_invalid_ticker()
        test_basic_generation()
    else:
        print("Invalid choice")
