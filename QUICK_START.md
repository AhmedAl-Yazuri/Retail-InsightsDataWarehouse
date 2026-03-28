# 🚀 Quick Start Guide

## One-Minute Setup

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure database (update config/db_config.json)

# 3. Launch dashboard
python launch_dashboard.py

# 4. Open browser to http://localhost:8501
```

---

## 📊 Available Tools

### 1. Interactive Dashboard
```bash
python launch_dashboard.py
```
**Perfect for:** Quick insights, exploration, presentations

**Includes 6 tabs:**
- 📊 Overview → KPIs, trends
- 💰 Sales Analysis → Weekly/monthly patterns
- 🏆 Top Performers → Best products/customers
- 📍 Regional Insights → Territory breakdown
- 👥 Customer Analytics → Behavior patterns
- ⚠️ Decline Analysis → 2016 vs 2017 deep dive

### 2. Storytelling Notebook
```bash
jupyter notebook notebooks/SalesDeclineStorytelling.ipynb
```
**Perfect for:** Deep analysis, reports, presentations

**Covers:**
- Why sales declined 1.4% (2016→2017)
- Root cause analysis
- Product/regional/customer insights
- Actionable recommendations

### 3. ETL Pipeline
```bash
python run.py
```
**Runs:**
1. Data ingestion
2. Data transformation
3. Data modeling
4. Statistics generation

---

## 🎯 Key Insights (Pre-Calculated)

### The Story
- **2016**: Peak year ($9.32M, 26,953 orders)
- **2017**: Slight decline ($9.18M, 26,481 orders, -1.4%)
- **Root Cause**: VOLUME decline, not pricing issue
- **AOV**: Actually increased (+$0.47) - customers buying MORE per transaction

### Quick Numbers
| Metric | 2016 | 2017 | Change |
|--------|------|------|--------|
| Sales | $9.32M | $9.18M | -1.4% |
| Orders | 26,953 | 26,481 | -1.8% |
| AOV | $346.35 | $346.82 | +0.1% |
| Customers | ~15.2K | ~15.8K | +4% |

### Opportunities
1. **Restore Transaction Volume** - Primary focus
2. **Regional Support** - Southwest/Northwest declining
3. **Product Revitalization** - Portfolio shifting
4. **Loyalty Programs** - Increase repeat purchases

---

## 💻 Common Commands

```bash
# Fresh data load
python scripts/Ingestion.py

# Transform data
python scripts/transformation.py

# Load to warehouse
python scripts/Modeling.py

# Generate stats
python scripts/Stats.py

# Run all steps
python run.py

# Start dashboard
python launch_dashboard.py

# Run notebook (analysis)
jupyter notebook notebooks/SalesDeclineStorytelling.ipynb

# View reports
open reports/stats_report.md
```

---

## 📂 Important Files

| File | Purpose |
|------|---------|
| `dashboard.py` | Main interactive dashboard app |
| `launch_dashboard.py` | Easy dashboard launcher |
| `notebooks/SalesDeclineStorytelling.ipynb` | Deep analysis notebook |
| `DASHBOARD_GUIDE.md` | Full dashboard documentation |
| `SALES_DECLINE_ANALYSIS.md` | Executive summary |
| `config/db_config.json` | Database connection (EDIT THIS) |
| `sql/queries.sql` | Available SQL queries |

---

## 🔑 Key Features

✅ Real-time interactive visualizations  
✅ Automatic chart generation  
✅ Multi-view dashboard  
✅ Deep-dive storytelling analysis  
✅ Professional report generation  
✅ SQL query library  
✅ Star schema data warehouse  

---

## ❓ I Want To...

**...explore sales data quickly**
→ Use the Dashboard (`python launch_dashboard.py`)

**...understand why sales declined**
→ Run the Storytelling Notebook

**...create a custom report**
→ Use SQL queries in `sql/queries.sql`

**...re-load the data**
→ Run `python run.py`

**...build my own analysis**
→ Check `notebooks/SalesDeclineStorytelling.ipynb` for examples

---

## 📈 Dashboard Tabs Overview

### 📊 Overview Tab
- **Total Sales**: $24.9M (all years)
- **Unique Customers**: 17,416
- **Total Orders**: 79,407
- **Avg Order Value**: $346.94
- **Sales Trend**: Monthly visualization
- **Year-over-Year Growth**: Calculated metrics

### 💰 Sales Analysis Tab
- Sales by weekday (identify peak days)
- Seasonal patterns
- Monthly analysis

### 🏆 Top Performers Tab
- Top 10 products by revenue
- Top 10 customers by spending
- Purchase frequency breakdown

### 📍 Regional Insights Tab
- Territory revenue distribution (treemap)
- Regional rankings
- Territory-level metrics

### 👥 Customer Analytics Tab
- Customer lifetime value distribution
- Purchase frequency patterns
- Segmentation insights

### ⚠️ Decline Analysis Tab
- 2016 vs 2017 comparison
- Product performance by year
- Regional performance comparison
- Root cause indicators

---

## 🎓 Learning Resources

1. **Start Here**: `README.md` (you're reading it!)
2. **Dashboard**: `DASHBOARD_GUIDE.md`
3. **Analysis**: `SALES_DECLINE_ANALYSIS.md`
4. **Notebook**: `SalesDeclineStorytelling.ipynb`
5. **SQL**: `sql/queries.sql`

---

## 💡 Pro Tips

💡 **Dashboard Tip**: Use "⚠️ Decline Analysis" tab for quick decline insights  
💡 **Notebook Tip**: Run all cells for comprehensive analysis with visuals  
💡 **Data Tip**: All analysis pulls from PostgreSQL warehouse in real-time  
💡 **Exploration Tip**: Combine dashboard + notebook for complete picture  

---

## 🐛 Troubleshooting

**Dashboard won't start:**
```bash
pip install streamlit plotly
python launch_dashboard.py
```

**Database connection failed:**
- Check `config/db_config.json`
- Verify PostgreSQL is running
- Confirm database exists

**Notebook won't load:**
```bash
pip install jupyter
jupyter notebook
# Navigate to notebooks/SalesDeclineStorytelling.ipynb
```

**Missing data:**
```bash
python run.py  # Re-run full ETL pipeline
```

---

## 📞 Need Help?

1. **For Dashboard**: See `DASHBOARD_GUIDE.md`
2. **For Analysis**: Run the Storytelling notebook
3. **For SQL**: Check `sql/queries.sql`
4. **For Setup**: Review README.md "Setup Instructions"

---

**Ready to Explore?**
```bash
python launch_dashboard.py
```

🚀 Let's find insights!
