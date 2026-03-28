# 📊 Dashboard & Storytelling Guide

## 🎯 Overview

This project now includes two powerful analysis tools for your Retail Insights Data Warehouse:

1. **Interactive Dashboard** - Real-time visualization of all key metrics
2. **Storytelling Notebook** - Deep-dive analysis of the 2016→2017 sales decline

---

## 🚀 Quick Start

### Launch the Interactive Dashboard

```bash
streamlit run dashboard.py
```

The dashboard will open at `http://localhost:8501` and provides:
- 📊 Overview with KPI cards
- 💰 Sales Analysis (trends, weekday patterns)  
- 🏆 Top Performers (products & customers)
- 📍 Regional Insights
- 👥 Customer Analytics
- ⚠️ Decline Analysis (2016 vs 2017)

### Run the Storytelling Analysis

Open in Jupyter:
```bash
jupyter notebook notebooks/SalesDeclineStorytelling.ipynb
```

---

## 📊 Dashboard Features

### 1️⃣ Overview Tab
**Metrics Displayed:**
- 💵 Total Sales: $24.9M
- 👥 Unique Customers: 17,416
- 📦 Total Orders: 79,407
- 💳 Average Order Value: $346.94

**Visualizations:**
- Monthly sales trend with interactive hover
- Year-over-year comparison
- Growth rates (2015→2016: +45.6%, 2016→2017: -1.4%)

### 2️⃣ Sales Analysis Tab
- 📊 Sales by Weekday (identify peak days)
- 📅 Seasonal patterns
- Distribution analysis

### 3️⃣ Top Performers Tab
- 🥇 Top 10 Products by Revenue
- 🎯 Top 10 Customers by Spending
- Purchase frequency data

### 4️⃣ Regional Insights Tab
- 🌍 Territory revenue treemap
- Performance rankings
- Territory-level metrics

### 5️⃣ Customer Analytics Tab
- 💰 Lifetime value distribution
- 🔄 Purchase frequency patterns
- Customer segmentation

### 6️⃣ Decline Analysis Tab ⚠️
**Key Focus Areas:**
- **Product-Level Analysis**: 2016 vs 2017 comparison
- **Regional Performance**: Territory-by-territory breakdown
- **Root Cause Indicators**: Volume vs. Price analysis

---

## 📉 Storytelling Analysis: Why Sales Declined

### The Story (Key Findings):

**Sales dropped 1.4% from 2016 to 2017 (-$134,648)**

#### Primary Cause: **VOLUME DECLINE**
```
2016 → 2017 Changes:
├── Orders: -472 (-1.8%)       ← PRIMARY DRIVER
├── Units Sold: Significant decrease
├── Avg Order Value: +$0.47 (+0.1%)  ← Customers buying MORE per transaction
└── Unique Customers: Slight decrease
```

#### Secondary Issues:
1. **Regional Disparities**
   - Some territories declined, others grew
   - Geographic imbalances visible

2. **Product Mix Shift**
   - Key products lost sales  
   - Portfolio rebalancing underway

3. **Customer Behavior**
   - Fewer transactions overall
   - Possible churn in order frequency

### The Good News ✅
- Average order value increased (quality focus)
- Some regions & products thriving
- Core fundamentals stable
- Decline is manageable (-1.4% is not catastrophic)

### Recommended Actions 🎬
1. **Customer Acquisition**: Restore transaction volume
2. **Regional Recovery**: Support declining territories
3. **Product Revitalization**: Promote underperforming products
4. **Loyalty Programs**: Increase repeat purchases
5. **Market Analysis**: Understand external competitive factors

---

## 🔧 Technical Details

### Dashboard Architecture
```
dashboard.py
├── Streamlit UI Framework
├── Plotly Visualizations (interactive charts)
├── SQLAlchemy Database Connection
└── Cached Data Loading (performance optimized)
```

**Key Features:**
- ✅ Caching for fast performance
- 📊 Interactive hover details
- 🎯 Multi-page navigation
- 📱 Responsive design
- 🔄 Real-time data from warehouse

### Storytelling Notebook Structure
```
SalesDeclineStorytelling.ipynb
├── Section 1: Year-over-Year Overview
├── Section 2: Monthly Deep Dive
├── Section 3: Product Analysis
├── Section 4: Regional Analysis
├── Section 5: Customer Behavior
├── Section 6: Price & Quantity Analysis
├── Section 7: Root Cause Summary
└── Section 8: Visual Dashboard & Conclusions
```

**Outputs Generated:**
- `reports/yearly_comparison.png` - KPI trends
- `reports/monthly_comparison.png` - Monthly patterns  
- `reports/product_analysis.png` - Product performance
- `reports/regional_analysis.png` - Territory insights
- `reports/summary_dashboard.png` - Executive summary

---

## 📈 Data Sources

All analyses pull from your data warehouse:
- **Fact Table**: `dw.fact_sales` (79,407 transactions)
- **Dimensions**: 
  - `dw.dim_customers` (17,416 customers)
  - `dw.dim_products` (~500 products)
  - `dw.dim_territories` (10 territories)
  - `dw.dim_calendar` (2015-2017)

---

## 🔍 Key SQL Queries Used

### Sales Trends
```sql
SELECT dc.year, SUM(fs.totalsales) 
FROM dw.fact_sales fs
JOIN dw.dim_calendar dc ON fs.dateid = dc.dateid
GROUP BY dc.year
ORDER BY dc.year
```

### Product Performance
```sql
SELECT dp.productname, 
       SUM(fs.totalsales) as sales_2016/2017,
       COUNT(fs.salesid) as order_count
FROM dw.fact_sales fs
JOIN dw.dim_products dp ON fs.productid = dp.productid
WHERE YEAR = 2016/2017
GROUP BY dp.productname
```

### Regional Analysis
```sql
SELECT dt.territoryname,
       SUM(fs.totalsales) as revenue,
       COUNT(DISTINCT fs.customerid) as unique_customers
FROM dw.fact_sales fs
JOIN dw.dim_territories dt ON fs.territoryid = dt.territoryid
GROUP BY dt.territoryname
```

---

## 📦 Dependencies

New requirements added to `requirements.txt`:
- **streamlit** (>=1.28.0) - Dashboard framework
- **plotly** (>=5.17.0) - Interactive visualizations
- **numpy** - Numerical analysis
- **scipy** - Statistical functions
- **matplotlib** & **seaborn** - Static visualizations
- Existing: pandas, sqlalchemy, psycopg2-binary, jupyter

---

## 🎓 Usage Examples

### Running Everything
```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run ETL pipeline (as before)
python run.py

# 3. Launch dashboard
streamlit run dashboard.py

# 4. Open storytelling notebook
jupyter notebook notebooks/SalesDeclineStorytelling.ipynb
```

### Quick Analysis
```python
# Open dashboard, navigate to "⚠️ Decline Analysis" tab
# Get instant insights about 2016 vs 2017 performance
```

### Deep Dive
```python
# Run storytelling notebook
# Get comprehensive root cause analysis with 8+ sections
# Generates professional visualizations
# Exportable as PDF for stakeholders
```

---

## 💡 Insights at a Glance

| Metric | 2016 | 2017 | Change |
|--------|------|------|--------|
| **Total Sales** | $9.32M | $9.18M | -1.4% |
| **Orders** | 26,953 | 26,481 | -1.8% |
| **Avg Order Value** | $346.35 | $346.82 | +0.1% |
| **Unique Customers** | ~17K | ~17K | Slight ↓ |
| **Top Territory** | Australia | Australia | Stable |
| **Top Product** | Water Bottle | Water Bottle | Stable |

---

## 🎯 Next Steps

1. **Review Dashboard** - Get familiar with all 6 tabs
2. **Run Storytelling** - Understand the decline analysis
3. **Investigate Further** - Focus on highest-impact areas
4. **Take Action** - Implement recommendations
5. **Monitor Progress** - Re-run analyses quarterly

---

## 📞 Questions?

For detailed analysis breakdown, see the Storytelling notebook.
For real-time exploration, use the interactive Dashboard.

**Both tools complement each other:**
- 📊 **Dashboard**: Quick insights & exploration
- 📉 **Storytelling**: Deep analysis & root causes
