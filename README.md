# Retail Insights Data Warehouse

A comprehensive data warehouse project for retail sales analytics, built with Python, PostgreSQL, and SQL.

## Project Overview

This project implements a data warehouse for retail sales data, including customer information, product catalogs, sales transactions, and geographical territories. It provides ETL processes, data modeling, and analytical reporting capabilities.

## Features

- **Data Ingestion**: Automated loading of raw CSV data into PostgreSQL staging tables
- **Data Transformation**: Cleaning and processing of data for warehouse schema
- **Data Modeling**: Star schema design for efficient analytics
- **Analytics & Reporting**: Statistical analysis and markdown reports generation
- **Exploratory Analysis**: Jupyter notebook for data exploration
- **🎯 Interactive Dashboard**: Real-time visualization of all metrics with 6 analytical views
- **📉 Storytelling Analysis**: Deep-dive investigation into the 2016→2017 sales decline

## Project Structure

```
├── config/                          # Configuration files for API and database
├── Data/
│   ├── raw/                        # Original CSV data files
│   └── processed/                  # Cleaned and transformed data
├── notebooks/                       # Jupyter notebooks for exploration
│   ├── Exploration.ipynb           # Data exploration
│   └── SalesDeclineStorytelling.ipynb  # Deep-dive decline analysis [NEW]
├── reports/                         # Generated reports and visualizations
├── scripts/                         # Python scripts for ETL and analysis
│   ├── Ingestion.py                # Data ingestion script
│   ├── transformation.py           # Data cleaning and transformation
│   ├── Modeling.py                 # Data modeling and warehouse loading
│   └── Stats.py                    # Statistical analysis and reporting
├── sql/                            # SQL schemas and queries
├── dashboard.py                    # Interactive Streamlit Dashboard [NEW]
├── launch_dashboard.py             # Dashboard launcher script [NEW]
├── run.py                          # Main ETL pipeline runner
├── DASHBOARD_GUIDE.md              # Dashboard documentation [NEW]
├── SALES_DECLINE_ANALYSIS.md       # Decline analysis summary [NEW]
├── requirements.txt                # Python dependencies
└── README.md                       # This file
```

## Setup Instructions

1. **Prerequisites**:
   - Python 3.8+
   - PostgreSQL database
   - Git

2. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd retail-insights-dw
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure database**:
   - Update `config/db_config.json` with your PostgreSQL credentials
   - Create the database if it doesn't exist

5. **Run the ETL pipeline**:
   ```bash
   # Option 1: Run all steps at once
   python run.py

   # Option 2: Run individual scripts
   python scripts/Ingestion.py
   python scripts/transformation.py
   python scripts/Modeling.py
   python scripts/Stats.py
   ```

## Data Sources

The project uses sample retail data including:
- Sales transactions (2015-2017)
- Customer demographics
- Product catalog and categories
- Geographical territories
- Return records
- Calendar data

## Usage

### Running the ETL Pipeline
```bash
python run.py
```

### 📊 Interactive Dashboard (NEW)
Launch a powerful interactive dashboard with 6 analytical views:
```bash
python launch_dashboard.py
# OR
streamlit run dashboard.py
```

Access at: `http://localhost:8501`

**Dashboard Features:**
- 📊 Overview with KPI cards
- 💰 Sales trends and patterns
- 🏆 Top products and customers
- 📍 Regional performance
- 👥 Customer analytics
- ⚠️ Sales decline analysis (2016 vs 2017)

### 📉 Storytelling Analysis (NEW)
Deep-dive investigation into why sales declined from 2016 to 2017:
```bash
jupyter notebook notebooks/SalesDeclineStorytelling.ipynb
```

**Includes:**
- Root cause analysis with multiple sections
- Product, regional, and customer insights
- 5+ professional visualizations
- Actionable recommendations

### Data Exploration
- **Interactive**: Open `notebooks/Exploration.ipynb` in Jupyter
- **Dashboard**: Use the interactive dashboard for real-time exploration
- **Reports**: Check `reports/stats_report.md` for generated analytics

### Custom Analysis
- Use `sql/queries.sql` as reference for additional analysis
- Check `DASHBOARD_GUIDE.md` for detailed documentation
- See `SALES_DECLINE_ANALYSIS.md` for decline insights

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.