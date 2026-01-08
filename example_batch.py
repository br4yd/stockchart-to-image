#!/usr/bin/env python3

"""
Example: Batch processing multiple stock tickers.
Useful for generating charts for multiple stocks at once.
"""

from stock_chart_generator import StockChartGenerator
from datetime import datetime


def generate_batch_charts(tickers: list[str], output_dir: str = "graphs"):
    """
    Generate charts for multiple tickers in batch.

    Args:
        tickers: List of ticker symbols
        output_dir: Output directory for charts
    """
    generator = StockChartGenerator(output_dir=output_dir)

    print(f"Batch Chart Generation - {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 60)
    print(f"Processing {len(tickers)} tickers...\n")

    results = {
        'success': [],
        'failed': []
    }

    for i, ticker in enumerate(tickers, 1):
        print(f"[{i}/{len(tickers)}] Processing {ticker}...")

        try:
            filepath = generator.generate(ticker)
            results['success'].append((ticker, filepath))
            print(f"  Success\n")

        except Exception as e:
            results['failed'].append((ticker, str(e)))
            print(f"  Failed: {str(e)}\n")

    print("=" * 60)
    print(f"\nSummary:")
    print(f"  Successful: {len(results['success'])}")
    print(f"  Failed: {len(results['failed'])}")

    if results['success']:
        print(f"\nSuccessfully generated charts:")
        for ticker, filepath in results['success']:
            print(f"  {ticker}: {filepath}")

    if results['failed']:
        print(f"\nFailed tickers:")
        for ticker, error in results['failed']:
            print(f"  {ticker}: {error}")

    return results


if __name__ == "__main__":
    us_tech_stocks = ['AAPL', 'MSFT', 'GOOGL', 'AMZN', 'META']

    us_index_funds = ['SPY', 'QQQ', 'DIA']

    european_stocks = ['ASML', 'SAP', 'SHELL']

    print("Select batch to process:")
    print("1. US Tech Stocks (AAPL, MSFT, GOOGL, AMZN, META)")
    print("2. US Index Funds (SPY, QQQ, DIA)")
    print("3. European Stocks (ASML, SAP, SHELL)")
    print("4. Custom (enter your own)")

    choice = input("\nEnter choice (1-4): ").strip()

    if choice == '1':
        tickers = us_tech_stocks
    elif choice == '2':
        tickers = us_index_funds
    elif choice == '3':
        tickers = european_stocks
    elif choice == '4':
        custom_input = input("Enter tickers separated by commas: ").strip()
        tickers = [t.strip().upper() for t in custom_input.split(',')]
    else:
        print("Invalid choice")
        exit(1)

    print()
    generate_batch_charts(tickers)
