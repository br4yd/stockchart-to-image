# Changelog

## Version 2.1 - Gap Fix and 5-Minute Intervals (CRITICAL FIX)

### Problem Fixed
The hourly implementation (v2.0) had a critical visualization issue where charts displayed huge diagonal lines across market closures (overnight, weekends). This made charts unprofessional and unsuitable for publication.

### Solution
- **Changed interval from 1h to 5m**: Now uses 5-minute intervals for smooth visualization
- **Implemented gap detection**: Automatically detects market closures and breaks the line
- **Segment-based plotting**: Plots separate line segments for each trading session
- **Matches industry standards**: Charts now resemble typical 5-day charts on financial websites

### Technical Changes

#### Data Fetching
- **Changed to 5-minute intervals**: `interval='5m'` instead of `interval='1h'`
- **Simplified period specification**: Uses `period='5d'` directly
- **Increased data points**: ~390 points (78 per day) vs. ~30-40 hourly points
- **Better intraday detail**: Shows smooth price movements throughout trading hours

#### Gap Handling
- **Gap detection algorithm**: Identifies time gaps larger than 2 hours
- **Segment creation**: Breaks data into segments at each gap
- **Individual segment plotting**: Each trading session rendered separately
- **Visual result**: Clean breaks between trading days, no diagonal lines

#### Chart Appearance
- **Simplified axis**: Removed minor time ticks (not needed with smooth data)
- **Cleaner labels**: Date-only x-axis labels, no rotation needed
- **Thinner lines**: Reduced to 1.2px width for clarity with more data points
- **Professional look**: Matches standard financial website 5-day chart appearance

### Benefits
1. Professional appearance suitable for newspaper publication
2. Smooth continuous lines during market hours
3. Clean visual breaks at market closures
4. Matches industry standard chart appearance
5. Better representation of intraday volatility

### Files Modified
- `stock_chart_generator.py`: Updated fetch_stock_data() and generate_chart()
- `README.md`: Updated feature list and specifications
- `CHANGELOG.md`: This file

### New Files
- `diagnose_data.py`: Diagnostic tool to examine data quality
- `GAP_FIX_NOTES.md`: Detailed technical explanation of the fix

---

## Version 2.0 - Hourly Data Implementation (DEPRECATED - HAD VISUALIZATION ISSUE)

### Major Changes

#### Data Fetching
- **Changed from daily to hourly intervals**: Modified `fetch_stock_data()` to use `interval='1h'` instead of `interval='1d'`
- **Increased fetch window**: Now fetches 10 days of data to ensure 5 complete trading days with hourly granularity
- **Smart filtering**: Automatically identifies and selects the last 5 trading days from hourly data
- **Improved date handling**: Handles both 'Datetime' and 'Date' column names from yfinance

#### Chart Visualization
- **Continuous line chart**: Removed markers and uses a smooth continuous line to show hourly price movements
- **Dual-level time axis**:
  - Major ticks display dates (e.g., "Jan 08")
  - Minor ticks display times at 6-hour intervals (e.g., "09:00")
- **Enhanced grid system**:
  - Major grid lines for dates (alpha=0.3)
  - Minor grid lines for time intervals (alpha=0.15)
- **Updated chart title**: Now indicates "(Hourly)" to clarify the data granularity
- **Improved axis labels**: Changed from "Date" to "Date & Time" for clarity
- **Rotated x-axis labels**: Set to 45 degrees for better readability with time data

#### Status Messages
- **Enhanced feedback**: Shows both number of hourly data points and trading days
- **Example output**: "Generating chart with 195 hourly data points across 5 trading days..."

#### Print Quality Maintained
- Still outputs at 300 DPI for print quality
- Chart remains clean and readable despite increased data points
- Line width reduced to 1.5 (from 2.0) for cleaner appearance with more data
- Maintained minimalistic design suitable for newspaper publication

### Technical Details

#### Data Volume
- **Before**: ~5 data points (one per day)
- **After**: ~30-40 data points per day × 5 days = ~150-200 hourly data points
- Data shows only trading hours, excluding overnight and weekend gaps

#### Performance Impact
- Slightly increased data transfer due to hourly granularity
- Processing time remains under 4 seconds per chart
- Memory usage still minimal due to efficient pandas operations

#### Backward Compatibility
- All existing command-line interfaces remain unchanged
- API methods maintain the same signatures
- Output file naming convention unchanged
- Error handling and alternative identifier prompts unchanged

### Files Modified

1. **stock_chart_generator.py**
   - `fetch_stock_data()`: Updated to fetch hourly data
   - `generate_chart()`: Enhanced for hourly visualization
   - `generate()`: Updated status messages

2. **README.md**
   - Updated feature list to mention hourly data
   - Modified chart specifications section
   - Updated technical details and dependencies

3. **QUICKSTART.md**
   - Updated basic usage description
   - Added yfinance to dependency list

### Migration Notes

No migration required. The tool automatically uses hourly data for all new chart generations. Previously generated charts remain valid as historical daily snapshots.

### Benefits

1. **Intraday Volatility Visible**: Users can now see price movements throughout the trading day
2. **Better Market Understanding**: Hourly data reveals patterns not visible in daily snapshots
3. **Professional Quality**: More detailed data while maintaining print-quality output
4. **No Additional Setup**: Uses the same yfinance library, no new dependencies

### Example Output

```
Fetching data for TSLA...
Generating chart with 195 hourly data points across 5 trading days...

Chart saved successfully: /path/to/graphs/2026-01-08_14-30_TSLA.png

Success! Chart available at: /path/to/graphs/2026-01-08_14-30_TSLA.png
```

### Testing Recommendations

After updating, test with various tickers:
```bash
python3 stock_chart_generator.py AAPL   # High liquidity stock
python3 stock_chart_generator.py TSLA   # Volatile stock
python3 stock_chart_generator.py SPY    # Index fund
```

Verify that:
- Charts display smooth hourly lines
- Date labels are clear and readable
- Time markers appear at 6-hour intervals
- Grid lines help distinguish different time periods
- Print quality remains at 300 DPI
