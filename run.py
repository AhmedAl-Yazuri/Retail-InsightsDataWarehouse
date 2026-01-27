#!/usr/bin/env python3
"""
Main runner script for the Retail Insights Data Warehouse ETL pipeline.
"""

import subprocess
import sys
import os

def run_script(script_name):
    """Run a Python script and check for errors."""
    script_path = os.path.join('scripts', script_name)
    print(f"Running {script_name}...")
    result = subprocess.run([sys.executable, script_path], capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Error in {script_name}:")
        print(result.stderr)
        sys.exit(1)
    else:
        print(f"{script_name} completed successfully.")

def main():
    """Run the complete ETL pipeline."""
    print("Starting Retail Insights Data Warehouse ETL Pipeline...")

    # Step 1: Data Ingestion
    run_script('Ingestion.py')

    # Step 2: Data Transformation
    run_script('transformation.py')

    # Step 3: Data Modeling
    run_script('Modeling.py')

    # Step 4: Generate Statistics
    run_script('Stats.py')

    print("ETL Pipeline completed successfully!")
    print("Check reports/stats_report.md for analytics results.")

if __name__ == "__main__":
    main()