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
        # Exact dimensions: 105.6mm x 44.45mm at 300 DPI = 1247px x 525px
        width_mm = 105.6
        height_mm = 44.45
        width_inch = width_mm / 25.4
        height_inch = height_mm / 25.4

        fig, ax = plt.subplots(figsize=(width_inch, height_inch), dpi=300)

        # Transparent background
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

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

            # Red price line (slightly thinner)
            ax.plot(x_smooth, y_smooth, linewidth=2.0, color='#FF0000',
                    linestyle='-', solid_capstyle='round', solid_joinstyle='round',
                    zorder=3)
        else:
            # Red price line (slightly thinner)
            ax.plot(x_indices, closes, linewidth=2.0, color='#FF0000',
                    linestyle='-', solid_capstyle='round', solid_joinstyle='round',
                    zorder=3)

        day_boundaries = []
        day_labels = []
        current_date = None

        for idx, row in data.iterrows():
            row_date = row['date_pd'].date()
            if row_date != current_date:
                day_boundaries.append(row['x_index'])
                # Format as "30 Jan" (day first, then month)
                day_labels.append(row['date_pd'].strftime('%d %b'))
                current_date = row_date

        label_positions = []
        for i in range(len(day_boundaries)):
            if i < len(day_boundaries) - 1:
                mid_point = (day_boundaries[i] + day_boundaries[i + 1]) / 2
            else:
                mid_point = (day_boundaries[i] + len(data) - 1) / 2
            label_positions.append(mid_point)

        ax.set_xticks(label_positions)
        # Bold x-axis labels
        ax.set_xticklabels(day_labels, fontweight='bold', fontsize=9)

        # Remove axis labels
        ax.set_xlabel('')
        ax.set_ylabel('')

        # Thin light-blue vertical gridlines
        ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, axis='x', color='#ADD8E6')
        ax.set_axisbelow(True)

        # Full-width dark blue header bar with company name
        from matplotlib.patches import FancyBboxPatch

        # Add header bar with rounded corners and shadow
        header_height = 0.08  # 8% of figure height

        # Shadow (slightly offset, semi-transparent)
        shadow_offset = 0.002
        shadow_rect = FancyBboxPatch((shadow_offset, 1 - header_height - shadow_offset),
                                     1 - shadow_offset, header_height,
                                     transform=fig.transFigure,
                                     boxstyle="round,pad=0,rounding_size=0.01",
                                     facecolor='black',
                                     edgecolor='none',
                                     alpha=0.15,
                                     zorder=9)
        fig.patches.append(shadow_rect)

        # Main header bar with 5px corner radius
        header_rect = FancyBboxPatch((0, 1 - header_height), 1, header_height,
                                     transform=fig.transFigure,
                                     boxstyle="round,pad=0,rounding_size=0.01",
                                     facecolor='#2d68b6',
                                     edgecolor='none',
                                     zorder=10)
        fig.patches.append(header_rect)

        # Add company name text left-aligned on header bar
        fig.text(0.03, 1 - header_height / 2, ticker.upper(),
                ha='left', va='center',
                fontsize=8, fontweight='bold',
                color='white',
                transform=fig.transFigure,
                zorder=11)

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

        # Remove top Y-axis labels that might overlap with header bar
        yticks = ax.get_yticks()
        y_labels = ax.get_yticklabels()
        # Hide the topmost label if it's in the upper 15% of the plot
        for i, (tick, label) in enumerate(zip(yticks, y_labels)):
            if tick > y_min + y_range * 0.85:
                label.set_visible(False)

        # Adjust layout to leave space for header bar at top
        plt.subplots_adjust(top=0.90, bottom=0.12, left=0.08, right=0.95)

        # Add current price indicator circle with collision detection
        current_price = closes[-1]

        # Get previous day's closing price for comparison
        prev_day_close = None
        if len(data) > 1:
            # Find the last data point of the previous day
            last_date = data['date_pd'].iloc[-1].date()
            prev_day_data = data[data['date_pd'].dt.date < last_date]
            if len(prev_day_data) > 0:
                prev_day_close = prev_day_data['close'].iloc[-1]

        if prev_day_close is not None:
            price_increased = current_price >= prev_day_close
            circle_color = '#00CC00' if price_increased else '#FF8C00'  # Green or orange

            # Find free space on the right side
            # Check if more space above or below the line at the right edge
            y_at_right = closes[-1]
            space_above = y_max + y_range * 0.1 - y_at_right
            space_below = y_at_right - (y_min - y_range * 0.1)

            # Position circle in the larger space
            if space_above > space_below:
                # Place above the line
                circle_y = y_at_right + space_above * 0.5
            else:
                # Place below the line
                circle_y = y_at_right - space_below * 0.5

            # Circle position (in data coordinates)
            circle_x = len(data) - 15  # 15 units from the right edge

            # Draw circle
            from matplotlib.patches import Circle
            circle_radius_x = 12  # x-axis units
            circle_radius_y = y_range * 0.08  # 8% of y-range

            circle = Circle((circle_x, circle_y), radius=circle_radius_y,
                          facecolor=circle_color, edgecolor='white',
                          linewidth=1.5, zorder=15, transform=ax.transData)
            ax.add_patch(circle)

            # Add text elements inside circle
            current_date = data['date_pd'].iloc[-1].strftime('%d %b')
            arrow = '▲' if price_increased else '▼'

            if price_increased:
                # Arrow above, date below
                ax.text(circle_x, circle_y + circle_radius_y * 0.35, arrow,
                       ha='center', va='center', fontsize=10,
                       color='#FFFF00', fontweight='bold', zorder=16)
                ax.text(circle_x, circle_y, f'{current_price:.2f}',
                       ha='center', va='center', fontsize=9,
                       color='white', fontweight='bold', zorder=16)
                ax.text(circle_x, circle_y - circle_radius_y * 0.35, current_date,
                       ha='center', va='center', fontsize=7,
                       color='#FFFF00', fontweight='bold', zorder=16)
            else:
                # Date above, arrow below
                ax.text(circle_x, circle_y + circle_radius_y * 0.35, current_date,
                       ha='center', va='center', fontsize=7,
                       color='#FFFF00', fontweight='bold', zorder=16)
                ax.text(circle_x, circle_y, f'{current_price:.2f}',
                       ha='center', va='center', fontsize=9,
                       color='white', fontweight='bold', zorder=16)
                ax.text(circle_x, circle_y - circle_radius_y * 0.35, arrow,
                       ha='center', va='center', fontsize=10,
                       color='#FFFF00', fontweight='bold', zorder=16)

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
                      facecolor='none', edgecolor='none', transparent=True)
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
