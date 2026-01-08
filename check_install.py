#!/usr/bin/env python3

"""
Installation verification script.
Checks that all dependencies are properly installed and functional.
"""

import sys
from pathlib import Path


def check_python_version():
    """Verify Python version is 3.8 or higher."""
    version = sys.version_info
    print(f"Python version: {version.major}.{version.minor}.{version.micro}")

    if version.major < 3 or (version.major == 3 and version.minor < 8):
        print("  ERROR: Python 3.8 or higher required")
        return False

    print("  OK")
    return True


def check_dependencies():
    """Verify all required packages are installed."""
    dependencies = {
        'pandas': '2.0.0',
        'matplotlib': '3.7.0'
    }

    all_ok = True

    for package, min_version in dependencies.items():
        try:
            module = __import__(package)
            version = getattr(module, '__version__', 'unknown')
            print(f"{package}: {version}")
            print("  OK")
        except ImportError:
            print(f"{package}: NOT INSTALLED")
            print(f"  ERROR: Install with 'pip install {package}>={min_version}'")
            all_ok = False

    return all_ok


def check_directory_structure():
    """Verify required directories exist."""
    script_dir = Path(__file__).parent.absolute()
    graphs_dir = script_dir / "graphs"

    print(f"Script directory: {script_dir}")
    print("  OK")

    if graphs_dir.exists():
        print(f"Output directory: {graphs_dir}")
        print("  OK")
    else:
        print("Output directory: Will be created on first run")
        print("  OK")

    return True


def check_network():
    """Verify network connectivity to Yahoo Finance."""
    import urllib.request
    import urllib.error

    try:
        url = "https://query1.finance.yahoo.com/v8/finance/chart/AAPL"
        with urllib.request.urlopen(url, timeout=5) as response:
            if response.status == 200:
                print("Network connectivity: Yahoo Finance API")
                print("  OK")
                return True
    except urllib.error.URLError as e:
        print("Network connectivity: FAILED")
        print(f"  ERROR: {str(e)}")
        return False
    except Exception as e:
        print("Network connectivity: FAILED")
        print(f"  ERROR: {str(e)}")
        return False


def main():
    """Run all installation checks."""
    print("Stock Chart Generator - Installation Check")
    print("=" * 60)
    print()

    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Directory Structure", check_directory_structure),
        ("Network Connectivity", check_network)
    ]

    results = []

    for name, check_func in checks:
        print(f"\nChecking {name}...")
        print("-" * 60)
        try:
            result = check_func()
            results.append(result)
        except Exception as e:
            print(f"  ERROR: {str(e)}")
            results.append(False)

    print("\n" + "=" * 60)
    print("Summary")
    print("=" * 60)

    if all(results):
        print("\nAll checks passed! Installation is ready.")
        print("\nTry running:")
        print("  python3 stock_chart_generator.py AAPL")
        return 0
    else:
        print("\nSome checks failed. Please review errors above.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
