#!/usr/bin/env python3

import os
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Optional, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import yfinance as yf
from scipy import interpolate


class StockChartGenerator:
    """Generate publication-quality stock charts for newspaper print media."""

    def __init__(self, output_dir: str = "graphs"):
        self.script_dir = Path(__file__).parent.absolute()
        self.output_dir = self.script_dir / output_dir
        self.output_dir.mkdir(exist_ok=True)

    def fetch_stock_data(self, ticker: str, days: int = 5) -> Optional[pd.DataFrame]:
        """
        Fetch intraday stock data from Yahoo Finance using yfinance library.
        Uses 5-minute intervals for smooth visualization of 5-day charts.

        Args:
            ticker: Stock ticker symbol
            days: Number of trading days to fetch (default 5)

        Returns:
            DataFrame with intraday stock data or None if fetch fails
        """
        try:
            stock = yf.Ticker(ticker)

            hist = stock.history(period='5d', interval='5m')

            if hist.empty:
                return None

            hist = hist.reset_index()

            if 'Datetime' in hist.columns:
                hist = hist.rename(columns={'Datetime': 'date'})
            elif 'Date' in hist.columns:
                hist = hist.rename(columns={'Date': 'date'})

            hist.columns = [col.lower() for col in hist.columns]
            hist = hist.dropna(subset=['close'])
            hist = hist.sort_values('date')

            if len(hist) == 0:
                return None

            return hist

        except Exception as e:
            return None

    def generate_chart(self, data: pd.DataFrame, ticker: str) -> plt.Figure:
        """
        Generate a print-quality stock chart with compressed x-axis.
        Uses numerical indices to eliminate empty space during market closures.

        Args:
            data: DataFrame containing intraday stock data
            ticker: Stock ticker symbol

        Returns:
            Matplotlib figure object
        """
        fig, ax = plt.subplots(figsize=(10, 6), dpi=300)

        data = data.copy()
        data['date_pd'] = pd.to_datetime(data['date'])
        data['x_index'] = range(len(data))

        x_indices = data['x_index'].values
        closes = data['close'].values
        y_min_global = closes.min()

        if len(x_indices) >= 4:
            cs = interpolate.CubicSpline(x_indices, closes, bc_type='natural')
            x_smooth = np.linspace(x_indices[0], x_indices[-1], len(x_indices) * 5)
            y_smooth = cs(x_smooth)

            ax.plot(x_smooth, y_smooth, linewidth=1.5, color='#2C3E50',
                    linestyle='-', solid_capstyle='round', solid_joinstyle='round',
                    zorder=3)

            ax.fill_between(x_smooth, y_smooth, y_min_global,
                           alpha=0.15, color='#2C3E50', zorder=2)
        else:
            ax.plot(x_indices, closes, linewidth=1.5, color='#2C3E50',
                    linestyle='-', solid_capstyle='round', solid_joinstyle='round',
                    zorder=3)

            ax.fill_between(x_indices, closes, y_min_global,
                           alpha=0.15, color='#2C3E50', zorder=2)

        day_boundaries = []
        day_labels = []
        current_date = None

        for idx, row in data.iterrows():
            row_date = row['date_pd'].date()
            if row_date != current_date:
                day_boundaries.append(row['x_index'])
                day_labels.append(row['date_pd'].strftime('%b %d'))
                current_date = row_date

        label_positions = []
        for i in range(len(day_boundaries)):
            if i < len(day_boundaries) - 1:
                mid_point = (day_boundaries[i] + day_boundaries[i + 1]) / 2
            else:
                mid_point = (day_boundaries[i] + len(data) - 1) / 2
            label_positions.append(mid_point)

        ax.set_xticks(label_positions)
        ax.set_xticklabels(day_labels)

        ax.set_xlabel('Date', fontsize=12, fontweight='bold')
        ax.set_ylabel('Price (USD)', fontsize=12, fontweight='bold')

        num_days = data['date_pd'].dt.date.nunique()
        ax.set_title(f'{ticker.upper()} - Last {num_days} Trading Days',
                     fontsize=14, fontweight='bold', pad=20)

        ax.grid(True, alpha=0.3, linestyle='--', linewidth=0.5, axis='y')
        ax.set_axisbelow(True)

        ax.spines['top'].set_visible(False)
        ax.spines['right'].set_visible(False)
        ax.spines['left'].set_linewidth(1.5)
        ax.spines['bottom'].set_linewidth(1.5)

        closes = data['close'].values
        y_min, y_max = closes.min(), closes.max()
        y_range = y_max - y_min
        ax.set_ylim(y_min - y_range * 0.1, y_max + y_range * 0.1)

        ax.set_xlim(-1, len(data))

        ax.tick_params(axis='both', which='major', labelsize=10)

        plt.tight_layout()

        return fig

    def save_chart(self, figure: plt.Figure, ticker: str) -> str:
        """
        Save chart to PNG file with timestamp.

        Args:
            figure: Matplotlib figure to save
            ticker: Stock ticker symbol

        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M')
        filename = f"{timestamp}_{ticker.upper()}.png"
        filepath = self.output_dir / filename

        figure.savefig(filepath, dpi=300, bbox_inches='tight',
                      facecolor='white', edgecolor='none')
        plt.close(figure)

        return str(filepath)

    def prompt_alternative_identifier(self) -> Tuple[str, str]:
        """
        Prompt user for alternative stock identifier.

        Returns:
            Tuple of (identifier_type, identifier_value)
        """
        print("\nTicker not found. Please provide an alternative identifier:")
        print("1. ISIN (International Securities Identification Number)")
        print("2. WKN (Wertpapierkennnummer)")
        print("3. Try a different ticker")

        choice = input("\nSelect option (1-3): ").strip()

        if choice == '1':
            isin = input("Enter ISIN: ").strip()
            return ('ISIN', isin)
        elif choice == '2':
            wkn = input("Enter WKN: ").strip()
            return ('WKN', wkn)
        elif choice == '3':
            ticker = input("Enter ticker: ").strip()
            return ('TICKER', ticker)
        else:
            raise ValueError("Invalid option selected")

    def convert_identifier_to_ticker(self, id_type: str, identifier: str) -> Optional[str]:
        """
        Attempt to convert ISIN/WKN to ticker symbol.

        Note: This is a simplified implementation. In production, you would
        use a dedicated API or database for identifier conversion.
        """
        if id_type == 'TICKER':
            return identifier

        print(f"\nNote: Direct {id_type} to ticker conversion requires additional APIs.")
        print("Please try entering the ticker symbol directly if known.")
        return None

    def generate(self, ticker: str) -> str:
        """
        Main method to generate stock chart.

        Args:
            ticker: Stock ticker symbol

        Returns:
            Path to generated chart file
        """
        print(f"Fetching data for {ticker.upper()}...")

        data = self.fetch_stock_data(ticker)

        if data is None or len(data) == 0:
            print(f"\nError: Could not fetch data for ticker '{ticker.upper()}'")

            id_type, identifier = self.prompt_alternative_identifier()
            converted_ticker = self.convert_identifier_to_ticker(id_type, identifier)

            if converted_ticker:
                data = self.fetch_stock_data(converted_ticker)
                if data is not None and len(data) > 0:
                    ticker = converted_ticker

            if data is None or len(data) == 0:
                raise ValueError(f"Unable to fetch data for the provided identifier")

        num_days = data['date'].dt.date.nunique()
        num_points = len(data)

        if num_days < 5:
            print(f"Warning: Only {num_days} trading days available (requested 5)")

        print(f"Generating chart with {num_points} data points across {num_days} trading days...")

        fig = self.generate_chart(data, ticker)
        filepath = self.save_chart(fig, ticker)

        print(f"\nChart saved successfully: {filepath}")

        return filepath


def main():
    """Command-line interface for stock chart generation."""
    if len(sys.argv) < 2:
        print("Usage: python stock_chart_generator.py <TICKER>")
        print("Example: python stock_chart_generator.py TSLA")
        sys.exit(1)

    ticker = sys.argv[1].strip().upper()

    try:
        generator = StockChartGenerator()
        filepath = generator.generate(ticker)
        print(f"\nSuccess! Chart available at: {filepath}")

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user")
        sys.exit(1)
    except Exception as e:
        print(f"\nError: {str(e)}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
