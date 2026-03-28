#!/usr/bin/env bash
# Quick setup script for Windows
# Run this in PowerShell to set up the dashboard environment

echo "================================"
echo "Setting up Retail Insights Dashboard"
echo "================================"
echo ""

echo "[1/3] Installing Python packages..."
pip install -r requirements.txt

echo ""
echo "[2/3] Setup complete!"
echo ""
echo "=========================================="
echo "To launch the dashboard, run:"
echo "=========================================="
echo ""
echo "  python launch_dashboard.py"
echo ""
echo "Or manually with:"
echo "  streamlit run dashboard.py"
echo ""
echo "=========================================="
echo ""
echo "To run the storytelling analysis:"
echo "  jupyter notebook notebooks/SalesDeclineStorytelling.ipynb"
echo ""
echo "=========================================="
echo ""
echo "For full documentation, see:"
echo "  - DASHBOARD_GUIDE.md"
echo "  - SALES_DECLINE_ANALYSIS.md"
echo ""
echo "✅ Setup complete!"
