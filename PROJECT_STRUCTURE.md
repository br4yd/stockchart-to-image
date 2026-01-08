# Project Structure

## File Overview

```
stocks-to-graph/
│
├── stock_chart_generator.py    # Main application (core functionality)
├── requirements.txt             # Python dependencies
│
├── README.md                    # Comprehensive documentation
├── QUICKSTART.md               # Quick start guide
├── PROJECT_STRUCTURE.md        # This file
│
├── setup.sh                    # Automated setup script
├── check_install.py            # Installation verification
│
├── test_generator.py           # Testing utilities
├── example_batch.py            # Batch processing example
│
├── .gitignore                  # Git ignore rules
└── graphs/                     # Output directory (auto-created)
    └── YYYY-MM-DD_HH-mm_TICKER.png
```

## Core Files

### stock_chart_generator.py
The main application containing:
- `StockChartGenerator` class
- Data fetching from Yahoo Finance API
- Chart generation with matplotlib
- File saving with timestamp naming
- Alternative identifier handling (ISIN/WKN)
- Command-line interface

**Usage**: `python3 stock_chart_generator.py <TICKER>`

### requirements.txt
Python package dependencies:
- pandas (data manipulation)
- matplotlib (chart generation)

**Usage**: `pip3 install -r requirements.txt`

## Documentation Files

### README.md
Complete documentation including:
- Feature overview
- Installation instructions
- Usage examples
- Chart specifications
- Error handling details
- Troubleshooting guide

### QUICKSTART.md
Quick reference for common tasks:
- Installation steps
- Common ticker examples
- Exchange suffix guide
- Quick troubleshooting

### PROJECT_STRUCTURE.md
This file - overview of project organization

## Utility Scripts

### setup.sh
Automated installation script:
- Checks Python version
- Installs dependencies
- Provides usage examples

**Usage**: `./setup.sh`

### check_install.py
Verifies installation health:
- Python version check
- Dependency verification
- Directory structure validation
- Network connectivity test

**Usage**: `python3 check_install.py`

### test_generator.py
Testing utilities:
- Basic chart generation tests
- Data fetch validation
- Invalid ticker handling
- Interactive test menu

**Usage**: `python3 test_generator.py`

### example_batch.py
Demonstrates batch processing:
- Multiple ticker processing
- Pre-defined ticker lists
- Custom ticker input
- Success/failure reporting

**Usage**: `python3 example_batch.py`

## Output Directory

### graphs/
Automatically created directory for chart output:
- Stores all generated PNG files
- Named with timestamp and ticker
- Excluded from git (see .gitignore)

**Format**: `YYYY-MM-DD_HH-mm_TICKER.png`

## Configuration Files

### .gitignore
Excludes from version control:
- Generated charts (graphs/)
- Python cache files
- Virtual environments
- IDE configuration
- OS-specific files

## Workflow

### First-time Setup
1. Clone/download project
2. Run `./setup.sh` or `pip3 install -r requirements.txt`
3. Verify with `python3 check_install.py`

### Daily Usage
1. Single chart: `python3 stock_chart_generator.py TICKER`
2. Batch processing: `python3 example_batch.py`
3. Find charts in `graphs/` directory

### Development
1. Modify `stock_chart_generator.py`
2. Test with `python3 test_generator.py`
3. Verify with real ticker: `python3 stock_chart_generator.py AAPL`

## Design Principles

### Modularity
- Core functionality in StockChartGenerator class
- Separate methods for fetch, process, generate, save
- Easy to extend and test

### Error Handling
- Graceful handling of network failures
- Invalid ticker detection
- Alternative identifier prompts
- Clear error messages

### Performance
- Efficient data fetching (single API call)
- Vectorized pandas operations
- Matplotlib optimization for print quality
- Minimal memory footprint

### Print Quality
- 300 DPI output
- Professional styling
- High contrast for readability
- Consistent formatting

## Technical Stack

- **Language**: Python 3.8+
- **Data Processing**: pandas
- **Visualization**: matplotlib
- **API**: Yahoo Finance (public, no key required)
- **Output Format**: PNG (300 DPI)

## Maintenance

### Updating Dependencies
```bash
pip3 install --upgrade pandas matplotlib
```

### Clearing Generated Charts
```bash
rm -rf graphs/*.png
```

### Running All Tests
```bash
python3 check_install.py
python3 test_generator.py
```
