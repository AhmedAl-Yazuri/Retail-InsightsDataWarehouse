#!/usr/bin/env python3
"""
Interactive Dashboard for Retail Insights Data Warehouse
Provides comprehensive visualization and analysis of retail sales data
"""

import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
from sqlalchemy import create_engine
import json
from datetime import datetime
import numpy as np

# Page Configuration
st.set_page_config(
    page_title="Retail Insights Dashboard",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main {
        padding-top: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1.5rem;
        border-radius: 0.5rem;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# Database Connection
@st.cache_resource
def get_db_connection():
    import os
    
    try:
        # Try Streamlit Secrets first
        if hasattr(st, 'secrets') and st.secrets:
            try:
                db_url = st.secrets['database']['url']
                if db_url:
                    # Convert to psycopg2 driver if needed
                    if db_url.startswith('postgresql://'):
                        db_url = db_url.replace('postgresql://', 'postgresql+psycopg2://', 1)
                    return create_engine(db_url)
            except (KeyError, TypeError):
                pass
        
        # Try local config file
        config_path = 'config/db_config.json'
        if os.path.exists(config_path):
            with open(config_path) as f:
                config = json.load(f)
            host = config.get('host', 'localhost')
            user = config.get('user', 'postgres')
            password = config.get('password', '')
            port = config.get('port', 5432)
            dbname = config.get('dbname', 'DATAW')
            DB_URI = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}"
            return create_engine(DB_URI)
        
        # If nothing works
        st.error("""
        ❌ **لم نعثر على بيانات الاتصال بقاعدة البيانات!**
        
        يرجى إضافة بيانات اتصال Railway PostgreSQL إلى Streamlit Cloud Secrets:
        
        1. اذهب إلى إعدادات التطبيق → Secrets
        2. أضف هذا:
        ```toml
        [database]
        url = "postgresql://postgres:IVYVDQWEMLzodIFDFxwsuFErkQrvdkcU@switchback.proxy.rlwy.net:10827/railway"
        ```
        3. اضغط Save
        4. انتظر 1 دقيقة
        5. اضغط Reboot app
        """)
        st.stop()
        
    except Exception as e:
        st.error(f"❌ خطأ في الاتصال: {str(e)}")
        st.stop()

@st.cache_data
def load_data(query):
    engine = get_db_connection()
    return pd.read_sql_query(query, engine)

# Page Title
st.title("📊 Retail Insights Dashboard")
st.markdown("---")

# Sidebar Filters
st.sidebar.title("🎯 Filters")
date_range = st.sidebar.date_input(
    "Select Date Range",
    value=(datetime(2015, 1, 1), datetime(2017, 12, 31)),
    help="Filter data by date range"
)

# Format dates for SQL
start_date = date_range[0].strftime('%Y-%m-%d')
end_date = date_range[1].strftime('%Y-%m-%d')

# Load Main Metrics
st.sidebar.markdown("---")
st.sidebar.title("📈 Quick Navigation")
page = st.sidebar.radio("Select View", [
    "📊 Overview",
    "💰 Sales Analysis",
    "🏆 Top Performers",
    "📍 Regional Insights",
    "👥 Customer Analytics",
    "⚠️ Decline Analysis"
])

# Query Templates
def get_overview_metrics(start_date, end_date):
    queries = {
        'total_sales': f"""
            SELECT SUM(totalsales)::NUMERIC AS total_sales 
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
        """,
        'unique_customers': f"""
            SELECT COUNT(DISTINCT fs.customerid)::INT AS unique_customers 
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
        """,
        'total_orders': f"""
            SELECT COUNT(*)::INT AS total_orders 
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
        """,
        'avg_order_value': f"""
            SELECT AVG(totalsales)::NUMERIC AS avg_order_value 
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
        """,
        'sales_by_year': f"""
            SELECT dc.year, SUM(fs.totalsales)::NUMERIC AS total_sales
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY dc.year
            ORDER BY dc.year
        """,
        'sales_by_month': f"""
            SELECT dc.year, dc.month, SUM(fs.totalsales)::NUMERIC AS total_sales
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY dc.year, dc.month
            ORDER BY dc.year, dc.month
        """
    }
    return queries

# PAGE 1: OVERVIEW
if page == "📊 Overview":
    st.header("Dashboard Overview")
    
    queries = get_overview_metrics(start_date, end_date)
    
    # Load metrics
    total_sales_data = load_data(queries['total_sales'])
    unique_customers_data = load_data(queries['unique_customers'])
    total_orders_data = load_data(queries['total_orders'])
    avg_order_value_data = load_data(queries['avg_order_value'])
    
    total_sales = total_sales_data.iloc[0, 0]
    unique_customers = unique_customers_data.iloc[0, 0]
    total_orders = total_orders_data.iloc[0, 0]
    avg_order_value = avg_order_value_data.iloc[0, 0]
    
    # KPI Cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric(
            label="💵 Total Sales",
            value=f"${total_sales:,.0f}",
            delta=None
        )
    
    with col2:
        st.metric(
            label="👥 Unique Customers",
            value=f"{unique_customers:,}",
            delta=None
        )
    
    with col3:
        st.metric(
            label="📦 Total Orders",
            value=f"{total_orders:,}",
            delta=None
        )
    
    with col4:
        st.metric(
            label="💳 Avg Order Value",
            value=f"${avg_order_value:,.2f}",
            delta=None
        )
    
    st.markdown("---")
    
    # Sales Trend
    st.subheader("📈 Sales Trend (2015-2017)")
    sales_by_month = load_data(queries['sales_by_month'])
    sales_by_month['date'] = pd.to_datetime(sales_by_month[['year', 'month']].assign(day=1))
    
    fig = px.line(
        sales_by_month,
        x='date',
        y='total_sales',
        markers=True,
        line_shape='spline',
        title='Monthly Sales Trend',
        labels={'date': 'Month', 'total_sales': 'Total Sales ($)'}
    )
    fig.update_layout(
        hovermode='x unified',
        template='plotly_white',
        height=400
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Sales by Year
    col1, col2 = st.columns(2)
    
    with col1:
        sales_by_year = load_data(queries['sales_by_year'])
        
        fig = px.bar(
            sales_by_year,
            x='year',
            y='total_sales',
            title='Yearly Sales Comparison',
            color='total_sales',
            color_continuous_scale='Blues',
            labels={'year': 'Year', 'total_sales': 'Total Sales ($)'}
        )
        fig.update_layout(template='plotly_white', height=400, showlegend=False)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("Year-over-Year Growth")
        
        years_data = sales_by_year.set_index('year')['total_sales']
        
        if len(years_data) >= 2:
            years_list = sorted(years_data.index.tolist())
            
            if len(years_list) >= 2:
                growth_1 = ((years_data[years_list[1]] - years_data[years_list[0]]) / years_data[years_list[0]] * 100)
                emoji_1 = "📈" if growth_1 >= 0 else "📉"
                st.write(f"**{years_list[0]} → {years_list[1]}:** {growth_1:+.1f}% {emoji_1}")
            
            if len(years_list) >= 3:
                growth_2 = ((years_data[years_list[2]] - years_data[years_list[1]]) / years_data[years_list[1]] * 100)
                emoji_2 = "📈" if growth_2 >= 0 else "📉"
                st.write(f"**{years_list[1]} → {years_list[2]}:** {growth_2:+.1f}% {emoji_2}")
        else:
            st.info("⚠️ Need at least 2 years of data for growth comparison")

# PAGE 2: SALES ANALYSIS
elif page == "💰 Sales Analysis":
    st.header("Sales Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📊 Sales by Weekday")
        query = f"""
            WITH weekday_sales_cte AS (
                SELECT 
                    dc.weekday, 
                    SUM(fs.totalsales)::NUMERIC AS total_sales
                FROM public.cleaned_sales fs
                JOIN public.calendar dc ON fs.dateid = dc.dateid
                WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY dc.weekday
            )
            SELECT * FROM weekday_sales_cte
            ORDER BY 
                CASE weekday
                    WHEN 'Sunday' THEN 1
                    WHEN 'Monday' THEN 2
                    WHEN 'Tuesday' THEN 3
                    WHEN 'Wednesday' THEN 4
                    WHEN 'Thursday' THEN 5
                    WHEN 'Friday' THEN 6
                    WHEN 'Saturday' THEN 7
                END
        """
        weekday_sales = load_data(query)
        
        fig = px.bar(
            weekday_sales,
            x='weekday',
            y='total_sales',
            color='total_sales',
            color_continuous_scale='Viridis',
            title='Sales by Weekday'
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📅 Sales by Month")
        query = f"""
            WITH monthly_sales_cte AS (
                SELECT 
                    dc.month, 
                    SUM(fs.totalsales)::NUMERIC AS total_sales
                FROM public.cleaned_sales fs
                JOIN public.calendar dc ON fs.dateid = dc.dateid
                WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY dc.month
            )
            SELECT * FROM monthly_sales_cte
            ORDER BY month
        """
        monthly_sales = load_data(query)
        
        month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']
        monthly_sales['month_name'] = monthly_sales['month'].apply(lambda x: month_names[int(x)-1])
        
        fig = px.line(
            monthly_sales,
            x='month_name',
            y='total_sales',
            markers=True,
            title='Seasonal Sales Pattern',
            labels={'month_name': 'Month', 'total_sales': 'Total Sales ($)'}
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)

# PAGE 3: TOP PERFORMERS
elif page == "🏆 Top Performers":
    st.header("Top Performers Analysis")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🥇 Top 10 Products by Sales")
        query = f"""
            WITH top_prods AS (
                SELECT 
                    dp.productname, 
                    COUNT(fs.salesid)::INT AS sales_count, 
                    SUM(fs.totalsales)::NUMERIC AS total_revenue
                FROM public.cleaned_sales fs
                JOIN public.products dp ON fs.productid = dp.productid
                JOIN public.calendar dc ON fs.dateid = dc.dateid
                WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY dp.productname
            )
            SELECT * FROM top_prods
            ORDER BY total_revenue DESC
            LIMIT 10
        """
        top_products = load_data(query)
        
        fig = px.bar(
            top_products,
            x='total_revenue',
            y='productname',
            orientation='h',
            color='total_revenue',
            color_continuous_scale='Greens',
            title='Top 10 Products by Revenue'
        )
        fig.update_layout(
            template='plotly_white',
            height=500,
            yaxis={'categoryorder': 'total ascending'}
        )
        st.plotly_chart(fig, use_container_width=True)

# PAGE 4: REGIONAL INSIGHTS
elif page == "📍 Regional Insights":
    st.header("Regional Performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🌍 Revenue by Territory")
        query = f"""
            WITH territory_revenue AS (
                SELECT 
                    dt.territoryname, 
                    SUM(fs.totalsales)::NUMERIC AS total_revenue, 
                    COUNT(fs.salesid)::INT AS order_count
                FROM public.cleaned_sales fs
                JOIN public.territories dt ON fs.territoryid = dt.territoryid
                JOIN public.calendar dc ON fs.dateid = dc.dateid
                WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
                GROUP BY dt.territoryname
            )
            SELECT * FROM territory_revenue
            ORDER BY total_revenue DESC
        """
        region_sales = load_data(query)
        
        fig = px.treemap(
            region_sales,
            labels='territoryname',
            values='total_revenue',
            color='total_revenue',
            color_continuous_scale='RdYlGn',
            title='Territory Revenue Distribution'
        )
        fig.update_layout(height=500)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("📊 Territories Ranking")
        st.dataframe(region_sales, use_container_width=True)

# PAGE 5: CUSTOMER ANALYTICS
elif page == "👥 Customer Analytics":
    st.header("Customer Analytics")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("💰 Customer Lifetime Value Distribution")
        query = """
            SELECT 
                dc.customerid,
                dc.customername,
                SUM(fs.totalsales)::NUMERIC AS lifetime_value,
                COUNT(fs.salesid)::INT AS purchase_count
            FROM public.cleaned_sales fs
            JOIN public.customers dc ON fs.customerid = dc.customerid
            GROUP BY dc.customerid, dc.customername
        """
        customer_ltv = load_data(query)
        
        fig = px.histogram(
            customer_ltv,
            x='lifetime_value',
            nbins=50,
            title='Customer Lifetime Value Distribution',
            color_discrete_sequence=['#636EFA']
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        st.subheader("🔄 Purchase Frequency Distribution")
        fig = px.histogram(
            customer_ltv,
            x='purchase_count',
            nbins=40,
            title='Customer Purchase Frequency',
            color_discrete_sequence=['#EF553B']
        )
        fig.update_layout(template='plotly_white', height=400)
        st.plotly_chart(fig, use_container_width=True)

# PAGE 6: DECLINE ANALYSIS  
elif page == "⚠️ Decline Analysis":
    st.header("2016 → 2017 Sales Decline Analysis")
    st.markdown("**Deep dive into the factors behind the sales decline**")
    st.markdown("---")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("📉 Yearly Comparison")
        query = f"""
            SELECT dc.year, SUM(fs.totalsales)::NUMERIC AS total_sales, COUNT(fs.salesid)::INT AS order_count
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            WHERE CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY dc.year
            ORDER BY dc.year
        """
        yearly = load_data(query)
        st.dataframe(yearly, use_container_width=True)
    
    with col2:
        st.metric("2017 vs 2016 Change", "-1.4%", "-$134,648")
    
    with col3:
        st.metric("Order Count 2016", "26,953", "")
        st.metric("Order Count 2017", "26,481", "-472")
    
    st.markdown("---")
    
    # Product-level decline analysis
    st.subheader("🏆 Product Performance: 2016 vs 2017")
    query = f"""
        WITH product_comparison AS (
            SELECT 
                dp.productname,
                SUM(CASE WHEN dc.year = 2016 THEN fs.totalsales ELSE 0 END)::NUMERIC AS sales_2016,
                SUM(CASE WHEN dc.year = 2017 THEN fs.totalsales ELSE 0 END)::NUMERIC AS sales_2017,
                COUNT(CASE WHEN dc.year = 2016 THEN fs.salesid END)::INT AS orders_2016,
                COUNT(CASE WHEN dc.year = 2017 THEN fs.salesid END)::INT AS orders_2017
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            JOIN public.products dp ON fs.productid = dp.productid
            WHERE dc.year IN (2016, 2017) AND CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY dp.productname
        )
        SELECT * FROM product_comparison
        ORDER BY (sales_2017 - sales_2016) DESC
        LIMIT 10
    """
    product_decline = load_data(query)
    product_decline['change'] = (product_decline['sales_2017'] - product_decline['sales_2016']) / product_decline['sales_2016'] * 100
    
    fig = px.bar(
        product_decline,
        x=['sales_2016', 'sales_2017'],
        y='productname',
        barmode='group',
        orientation='h',
        title='Top Products: Sales Comparison 2016 vs 2017',
        labels={'value': 'Sales ($)'}
    )
    fig.update_layout(
        template='plotly_white',
        height=500,
        yaxis={'categoryorder': 'total ascending'}
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Regional decline analysis
    st.subheader("📍 Regional Performance: 2016 vs 2017")
    query = f"""
        WITH region_comparison AS (
            SELECT 
                dt.territoryname,
                SUM(CASE WHEN dc.year = 2016 THEN fs.totalsales ELSE 0 END)::NUMERIC AS sales_2016,
                SUM(CASE WHEN dc.year = 2017 THEN fs.totalsales ELSE 0 END)::NUMERIC AS sales_2017
            FROM public.cleaned_sales fs
            JOIN public.calendar dc ON fs.dateid = dc.dateid
            JOIN public.territories dt ON fs.territoryid = dt.territoryid
            WHERE dc.year IN (2016, 2017) AND CAST(CONCAT(dc.year, '-', LPAD(dc.month::TEXT, 2, '0'), '-', LPAD(dc.day::TEXT, 2, '0')) AS DATE) BETWEEN '{start_date}' AND '{end_date}'
            GROUP BY dt.territoryname
        )
        SELECT * FROM region_comparison
        ORDER BY sales_2016 DESC
    """
    region_decline = load_data(query)
    region_decline['change'] = ((region_decline['sales_2017'] - region_decline['sales_2016']) / region_decline['sales_2016'] * 100).round(2)
    
    fig = px.bar(
        region_decline,
        x=['sales_2016', 'sales_2017'],
        y='territoryname',
        barmode='group',
        orientation='h',
        title='Territory Sales: 2016 vs 2017 Comparison'
    )
    fig.update_layout(template='plotly_white', height=400)
    st.plotly_chart(fig, use_container_width=True)
    
    st.dataframe(region_decline, use_container_width=True)

st.sidebar.markdown("---")
st.sidebar.markdown("📧 **Dashboard Built with Streamlit & Plotly**")
