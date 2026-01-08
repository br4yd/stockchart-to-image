#!/bin/bash

echo "Stock Chart Generator - Setup Script"
echo "====================================="
echo ""

echo "Checking Python version..."
python3 --version

if [ $? -ne 0 ]; then
    echo "Error: Python 3 is not installed"
    exit 1
fi

echo ""
echo "Creating virtual environment..."
python3 -m venv venv

if [ $? -ne 0 ]; then
    echo "Error: Failed to create virtual environment"
    exit 1
fi

echo ""
echo "Activating virtual environment..."
source venv/bin/activate

echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

if [ $? -eq 0 ]; then
    echo ""
    echo "Setup completed successfully!"
    echo ""
    echo "IMPORTANT: To use the tool, activate the virtual environment first:"
    echo "  source venv/bin/activate"
    echo ""
    echo "Then run:"
    echo "  python stock_chart_generator.py <TICKER>"
    echo ""
    echo "Example:"
    echo "  source venv/bin/activate"
    echo "  python stock_chart_generator.py TSLA"
    echo ""
    echo "To deactivate the virtual environment when done:"
    echo "  deactivate"
else
    echo ""
    echo "Error: Failed to install dependencies"
    exit 1
fi
