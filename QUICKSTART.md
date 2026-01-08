# Quick Start Guide

## Installation

1. Run the setup script:
```bash
./setup.sh
```

This will create a virtual environment and install dependencies.

Or manually:
```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## Basic Usage

1. Activate the virtual environment:
```bash
source venv/bin/activate
```

2. Generate a single stock chart:
```bash
python stock_chart_generator.py TSLA
```

3. Deactivate when done:
```bash
deactivate
```

The chart will be saved to `graphs/2026-01-08_14-30_TSLA.png`

## Common Examples

### US Stocks
```bash
python stock_chart_generator.py AAPL    # Apple
python stock_chart_generator.py MSFT    # Microsoft
python stock_chart_generator.py TSLA    # Tesla
python stock_chart_generator.py GOOGL   # Google
```

### European Stocks
```bash
python stock_chart_generator.py ASML    # ASML Holding
python stock_chart_generator.py SAP     # SAP SE
python stock_chart_generator.py SHELL   # Shell
```

### UK Stocks (London Stock Exchange)
```bash
python stock_chart_generator.py LLOY.L   # Lloyd's Banking Group
python stock_chart_generator.py BP.L     # BP
python stock_chart_generator.py HSBA.L   # HSBC
```

### German Stocks (XETRA)
```bash
python stock_chart_generator.py BMW.DE   # BMW
python stock_chart_generator.py VOW.DE   # Volkswagen
python stock_chart_generator.py SIE.DE   # Siemens
```

## Batch Processing

Generate multiple charts at once:
```bash
python example_batch.py
```

## Testing

Run the test suite:
```bash
python test_generator.py
```

## Programmatic Usage

```python
from stock_chart_generator import StockChartGenerator

generator = StockChartGenerator()
filepath = generator.generate("AAPL")
print(f"Chart saved: {filepath}")
```

## Output Location

All charts are saved to the `graphs/` directory:
```
graphs/
├── 2026-01-08_14-30_AAPL.png
├── 2026-01-08_14-31_MSFT.png
└── 2026-01-08_14-32_TSLA.png
```

## Troubleshooting

### Ticker not found
Add the appropriate exchange suffix:
- London: `.L` (e.g., LLOY.L)
- Germany: `.DE` (e.g., BMW.DE)
- Paris: `.PA` (e.g., MC.PA)

### Dependencies not installed
Activate virtual environment first:
```bash
source venv/bin/activate
pip install pandas matplotlib
```

### Permission denied on setup.sh
Run: `chmod +x setup.sh`
