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
        width_mm = 105.6
        height_mm = 44.45
        width_inch = width_mm / 25.4
        height_inch = height_mm / 25.4

        fig, ax = plt.subplots(figsize=(width_inch, height_inch), dpi=300)

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

            ax.plot(x_smooth, y_smooth, linewidth=2.0, color='#FF0000',
                    linestyle='-', solid_capstyle='round', solid_joinstyle='round',
                    zorder=3)
        else:
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
                day_labels.append(row['date_pd'].strftime('%d %b'))
                current_date = row_date

        label_positions = []
        for i in range(len(day_boundaries)):
            if i < len(day_boundaries) - 1:
                mid_point = (day_boundaries[i] + day_boundaries[i + 1]) / 2
            else:
                mid_point = (day_boundaries[i] + len(data) - 1) / 2
            label_positions.append(mid_point)

        filtered_positions = []
        filtered_labels = []
        min_distance = 50

        for i in range(len(label_positions)):
            if i == len(label_positions) - 1:
                filtered_positions.append(label_positions[i])
                filtered_labels.append(day_labels[i])
            elif i < len(label_positions) - 1:
                distance = label_positions[i + 1] - label_positions[i]
                if distance >= min_distance:
                    filtered_positions.append(label_positions[i])
                    filtered_labels.append(day_labels[i])

        ax.set_xticks(filtered_positions)
        ax.set_xticklabels(filtered_labels, fontweight='bold', fontsize=9)

        ax.set_xlabel('')
        ax.set_ylabel('')

        ax.grid(True, alpha=0.4, linestyle='-', linewidth=0.5, axis='x', color='#ADD8E6')
        ax.set_axisbelow(True)

        from matplotlib.patches import Rectangle

        header_height = 0.08
        shadow_offset = 0.002

        shadow_rect = Rectangle((shadow_offset, 1 - header_height - shadow_offset),
                                1 - shadow_offset, header_height,
                                transform=fig.transFigure,
                                facecolor='black',
                                edgecolor='none',
                                alpha=0.15,
                                zorder=9)
        fig.patches.append(shadow_rect)

        header_rect = Rectangle((0, 1 - header_height), 1, header_height,
                               transform=fig.transFigure,
                               facecolor='#2d68b6',
                               edgecolor='none',
                               zorder=10)
        fig.patches.append(header_rect)

        fig.text(0.05, 1 - header_height / 2, ticker.upper(),
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

        plt.subplots_adjust(top=0.85, bottom=0.15, left=0.12, right=0.95)

        current_price = closes[-1]

        prev_day_close = None
        if len(data) > 1:
            last_date = data['date_pd'].iloc[-1].date()
            prev_day_data = data[data['date_pd'].dt.date < last_date]
            if len(prev_day_data) > 0:
                prev_day_close = prev_day_data['close'].iloc[-1]

        if prev_day_close is not None:
            price_increased = current_price >= prev_day_close
            circle_color = '#00CC00' if price_increased else '#FF8C00'

            closes = data['close'].values
            y_at_right = closes[-1]
            space_above = (y_max + y_range * 0.1) - y_at_right
            space_below = y_at_right - (y_min - y_range * 0.1)

            if space_above > space_below:
                circle_y = y_at_right + space_above * 0.6
            else:
                circle_y = y_at_right - space_below * 0.6

            circle_x = len(data) - 35

            current_date = data['date_pd'].iloc[-1].strftime('%d %b')
            arrow = '▲' if price_increased else '▼'

            from matplotlib.patches import Ellipse

            x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
            y_display_range = ax.get_ylim()[1] - ax.get_ylim()[0]

            fig_width, fig_height = fig.get_size_inches()
            ax_width = (0.95 - 0.12) * fig_width
            ax_height = (0.85 - 0.15) * fig_height
            aspect_ratio = (x_range / y_display_range) * (ax_height / ax_width)

            circle_height = y_range * 0.45
            circle_width = circle_height * aspect_ratio

            circle = Ellipse((circle_x, circle_y), width=circle_width, height=circle_height,
                           facecolor=circle_color, edgecolor='white',
                           linewidth=1.0, zorder=15)
            ax.add_patch(circle)

            circle_radius = circle_height

            if price_increased:
                ax.text(circle_x, circle_y + circle_radius * 0.30, arrow,
                       ha='center', va='center', fontsize=8,
                       color='#FFFF00', fontweight='bold', zorder=17)
                ax.text(circle_x, circle_y, f'{current_price:.2f}',
                       ha='center', va='center', fontsize=6.5,
                       color='white', fontweight='bold', zorder=17)
                ax.text(circle_x, circle_y - circle_radius * 0.25, current_date,
                       ha='center', va='center', fontsize=5.5,
                       color='#FFFF00', fontweight='bold', zorder=17)
            else:
                ax.text(circle_x, circle_y + circle_radius * 0.25, current_date,
                       ha='center', va='center', fontsize=5.5,
                       color='#FFFF00', fontweight='bold', zorder=17)
                ax.text(circle_x, circle_y, f'{current_price:.2f}',
                       ha='center', va='center', fontsize=6.5,
                       color='white', fontweight='bold', zorder=17)
                ax.text(circle_x, circle_y - circle_radius * 0.25, arrow,
                       ha='center', va='center', fontsize=8,
                       color='#FFFF00', fontweight='bold', zorder=17)

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

        figure.savefig(filepath, dpi=300,
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
