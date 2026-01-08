# Stock Chart Generator for Print Media

A professional Python tool for generating publication-quality stock price charts suitable for newspaper and print media.

## Features

- Fetches real-time hourly stock data from Yahoo Finance using yfinance library
- Generates clean, minimalistic charts optimized for print media
- Produces 300 DPI PNG files suitable for professional publication
- Displays hourly price changes over the last 5 trading days
- Shows intraday volatility with detailed time-based data points
- Handles invalid tickers with alternative identifier prompts (ISIN/WKN)
- Automatic timestamp-based file naming
- Robust error handling and validation

## Installation

1. Ensure Python 3.8 or higher is installed:
```bash
python3 --version
```

2. Install required dependencies:
```bash
pip install -r requirements.txt
```

## Usage

### Command Line

```bash
python stock_chart_generator.py <TICKER>
```

### Examples

```bash
# Generate chart for Tesla
python stock_chart_generator.py TSLA

# Generate chart for Lloyd's Banking Group
python stock_chart_generator.py LLOY

# Generate chart for Apple
python stock_chart_generator.py AAPL
```

### Output

Charts are saved to the `graphs/` directory with the following naming convention:
```
YYYY-MM-DD_HH-mm_<TICKER>.png
```

Example: `2026-01-08_14-30_TSLA.png`

### Programmatic Usage

```python
from stock_chart_generator import StockChartGenerator

generator = StockChartGenerator(output_dir="graphs")
filepath = generator.generate("TSLA")
print(f"Chart saved to: {filepath}")
```

## Chart Specifications

- **Resolution**: 300 DPI (print quality)
- **Format**: PNG with white background
- **Size**: 10x6 inches (3000x1800 pixels)
- **Style**: Continuous line chart showing hourly data
- **Color Scheme**: Professional grayscale (#2C3E50)
- **Data Interval**: Hourly prices over 5 trading days
- **Time Display**: Major ticks show dates, minor ticks show 6-hour intervals
- **Elements**: Title with hourly notation, date/time axis, price axis, dual-level grid lines

## Error Handling

### Invalid Ticker
If a ticker is not found, the tool will prompt for alternative identifiers:
1. ISIN (International Securities Identification Number)
2. WKN (Wertpapierkennnummer - German securities ID)
3. Alternative ticker symbol

### Network Issues
- Automatic timeout after 10 seconds
- Clear error messages for connection failures
- Graceful handling of API rate limits

### Insufficient Data
If fewer than 5 trading days are available (e.g., newly listed stocks), the tool:
- Displays a warning message
- Generates a chart with available data
- Continues execution successfully

## Technical Details

### Data Source
Yahoo Finance via yfinance library - Hourly interval data with 1h granularity

### Dependencies
- `pandas` - Data manipulation and analysis
- `matplotlib` - Chart generation and rendering
- `yfinance` - Yahoo Finance data retrieval

### Performance
- Average execution time: 2-4 seconds per chart
- Memory efficient handling of hourly time-series data
- Optimized vectorized operations
- Fetches 10 days of data to ensure 5 complete trading days

## File Structure

```
stocks-to-graph/
├── stock_chart_generator.py    # Main application
├── requirements.txt             # Python dependencies
├── README.md                    # Documentation
└── graphs/                      # Output directory (auto-created)
    └── YYYY-MM-DD_HH-mm_TICKER.png
```

## Supported Exchanges

The tool supports tickers from major global exchanges including:
- NYSE (New York Stock Exchange)
- NASDAQ
- LSE (London Stock Exchange) - use .L suffix (e.g., LLOY.L)
- XETRA (Frankfurt) - use .DE suffix (e.g., BMW.DE)
- And many others supported by Yahoo Finance

### Exchange Suffix Examples
```bash
python stock_chart_generator.py LLOY.L    # London Stock Exchange
python stock_chart_generator.py BMW.DE    # Frankfurt/XETRA
python stock_chart_generator.py TSLA      # US exchanges (no suffix needed)
```

## Troubleshooting

### "Could not fetch data for ticker"
- Verify the ticker symbol is correct
- Check if an exchange suffix is needed (.L, .DE, etc.)
- Ensure internet connection is active
- Try an alternative identifier (ISIN/WKN)

### "Module not found" errors
Run: `pip install -r requirements.txt`

### Charts appear pixelated
The tool generates 300 DPI images. Ensure your viewer is not downscaling the image.

## License

This tool is provided as-is for newspaper and publication workflows.
