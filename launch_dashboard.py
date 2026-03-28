#!/usr/bin/env python3
"""
Launcher script for the Retail Insights Dashboard and Analysis
Run this to start the interactive dashboard
"""

import subprocess
import sys
import webbrowser
import time
import os
from pathlib import Path

def main():
    """Launch the Streamlit dashboard."""
    
    print("\n" + "="*70)
    print("🚀 RETAIL INSIGHTS DASHBOARD LAUNCHER")
    print("="*70)
    print("\n📊 Starting interactive dashboard...")
    print("\n⏳ Dashboard will open at: http://localhost:8501")
    print("\nPress Ctrl+C to stop the dashboard\n")
    
    # Verify we're in the right directory
    if not Path("dashboard.py").exists():
        print("❌ Error: dashboard.py not found in current directory")
        print(f"   Current directory: {os.getcwd()}")
        sys.exit(1)
    
    # Give a moment before opening browser
    time.sleep(2)
    
    # Try to open browser automatically
    try:
        webbrowser.open('http://localhost:8501', new=2)
        print("🌐 Browser opened automatically\n")
    except:
        print("💡 Please manually open: http://localhost:8501\n")
    
    # Launch streamlit
    try:
        print(f"Running: {sys.executable} -m streamlit run dashboard.py\n")
        subprocess.run([sys.executable, "-m", "streamlit", "run", "dashboard.py"])
    except KeyboardInterrupt:
        print("\n\n✅ Dashboard stopped")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ Error launching dashboard: {e}")
        print("\n💡 If you see 'No module named streamlit', run:")
        print("   python -m pip install streamlit plotly")
        print("\n   Or if using venv:")
        print("   .\\venv\\Scripts\\python -m pip install streamlit plotly")
        sys.exit(1)

if __name__ == "__main__":
    main()
