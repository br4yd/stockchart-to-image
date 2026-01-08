#!/usr/bin/env python3

"""
Diagnostic tool to examine the stock data being fetched.
Shows intervals, gaps, and data quality metrics.
"""

import yfinance as yf
import pandas as pd
from datetime import datetime


def diagnose_ticker(ticker: str):
    """
    Fetch and analyze stock data for a given ticker.
    """
    print(f"Diagnosing ticker: {ticker.upper()}")
    print("=" * 60)

    stock = yf.Ticker(ticker)

    print("\nFetching 5-day data with 5-minute intervals...")
    hist = stock.history(period='5d', interval='5m')

    if hist.empty:
        print("ERROR: No data returned")
        return

    hist = hist.reset_index()
    print(f"Total data points: {len(hist)}")

    if 'Datetime' in hist.columns:
        date_col = 'Datetime'
    elif 'Date' in hist.columns:
        date_col = 'Date'
    else:
        print("ERROR: No date column found")
        return

    hist['date'] = pd.to_datetime(hist[date_col])

    num_days = hist['date'].dt.date.nunique()
    print(f"Trading days covered: {num_days}")

    print(f"\nFirst data point: {hist['date'].iloc[0]}")
    print(f"Last data point: {hist['date'].iloc[-1]}")

    print("\nData points per day:")
    for date, group in hist.groupby(hist['date'].dt.date):
        print(f"  {date}: {len(group)} points")

    print("\nTime gaps analysis:")
    hist['time_diff'] = hist['date'].diff()

    large_gaps = hist[hist['time_diff'] > pd.Timedelta(hours=1)]
    print(f"Gaps larger than 1 hour: {len(large_gaps)}")

    if len(large_gaps) > 0:
        print("\nLarge gaps found:")
        for idx, row in large_gaps.head(10).iterrows():
            prev_idx = idx - 1
            if prev_idx >= 0:
                prev_time = hist.loc[prev_idx, 'date']
                curr_time = row['date']
                gap_hours = row['time_diff'].total_seconds() / 3600
                print(f"  {prev_time} -> {curr_time} (Gap: {gap_hours:.1f} hours)")

    print("\nInterval distribution:")
    intervals = hist['time_diff'].value_counts().head(5)
    for interval, count in intervals.items():
        if pd.notna(interval):
            minutes = interval.total_seconds() / 60
            print(f"  {minutes:.0f} minutes: {count} occurrences")

    print("\nPrice statistics:")
    print(f"  Open: ${hist['Open'].iloc[0]:.2f}")
    print(f"  Close: ${hist['Close'].iloc[-1]:.2f}")
    print(f"  High: ${hist['High'].max():.2f}")
    print(f"  Low: ${hist['Low'].min():.2f}")
    print(f"  Range: ${hist['High'].max() - hist['Low'].min():.2f}")

    print("\nSample data (first 10 points):")
    print(hist[['date', 'Open', 'High', 'Low', 'Close']].head(10).to_string())

    print("\n" + "=" * 60)
    print("Diagnosis complete")


if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python diagnose_data.py <TICKER>")
        print("Example: python diagnose_data.py AAPL")
        sys.exit(1)

    ticker = sys.argv[1].strip().upper()

    try:
        diagnose_ticker(ticker)
    except Exception as e:
        print(f"Error: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
