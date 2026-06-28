import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Set up a wide webpage canvas right out of the gate
st.set_page_config(page_title="Retail Operations Dashboard", layout="wide")

# --- CUSTOM CSS FOR ENHANCED VISIBILITY ---
st.markdown("""
    <style>
    /* Pump up the main title size */
    h1 {
        font-size: 2.8rem !important;
        font-weight: 800 !important;
    }
    /* Make section subheaders prominent and clean */
    h3 {
        font-size: 1.8rem !important;
        font-weight: 700 !important;
        margin-top: 25px !important;
    }
    /* Make metric descriptions clearly visible */
    [data-testid="stMetricLabel"] {
        font-size: 1.15rem !important;
        font-weight: 600 !important;
        color: #444444 !important;
    }
    /* Crank up the main scorecard numbers so they pop */
    [data-testid="stMetricValue"] {
        font-size: 2.5rem !important;
        font-weight: 800 !important;
    }
    /* Enlarge navigation tab text labels */
    button[data-baseweb="tab"] p {
        font-size: 1.25rem !important;
        font-weight: 600 !important;
    }
    /* Clean up default descriptions font size */
    .stMarkdown p {
        font-size: 1.1rem !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title("📊 Online Retail Global Operations & Customer Analytics")
st.markdown("An interactive workspace to effortlessly track macro sales trends, hourly checkout habits, and customer lifetime value metrics.")


# 1. DATA OPTIMIZATION: Crunch and compress ALL summaries inside the cache memory upfront
@st.cache_data
def load_and_preaggregate_data():
    df = pd.read_parquet("online_retail_ii_clean.parquet")
    df["InvoiceDate"] = pd.to_datetime(df["InvoiceDate"])
    
    # Bake time fields into the primary dataframe quickly
    df["Order_Month"] = df["InvoiceDate"].dt.strftime("%Y-%m")
    df["Calendar_Month"] = df["InvoiceDate"].dt.strftime("%b")
    df["Month_Num"] = df["InvoiceDate"].dt.month
    df["Hour"] = df["InvoiceDate"].dt.hour
    df["Day_of_Week"] = df["InvoiceDate"].dt.day_name()
    
    # --- PRE-AGGREGATING MINI TABLES FOR REAL-TIME INSTANT LOADING ---
    countries = ["All"] + sorted(df["Country"].unique().tolist())
    
    monthly_summary = df.groupby(["Country", "Order_Month"]).agg(
        Revenue=("Revenue", "sum"),
        Orders=("Invoice", "nunique")
    ).reset_index()
    
    seasonal_summary = df.groupby(["Country", "Month_Num", "Calendar_Month"], observed=False).agg(
        Revenue=("Revenue", "sum")
    ).reset_index()
    
    product_summary = df.groupby(["Country", "Description"]).agg(
        Quantity=("Quantity", "sum")
    ).reset_index()
    
    hourly_summary = df.groupby(["Country", "Hour"]).agg(
        Orders=("Invoice", "nunique")
    ).reset_index()
    
    daily_summary = df.groupby(["Country", "Day_of_Week"]).agg(
        Orders=("Invoice", "nunique")
    ).reset_index()
    
    max_date = df["InvoiceDate"].max() + pd.Timedelta(days=1)
    cust_base = df[df["CustomerID"].notnull()]
    rfm_master = cust_base.groupby(["Country", "CustomerID"]).agg(
        Last_Purchase=("InvoiceDate", "max"),
        Frequency=("Invoice", "nunique"),
        Monetary=("Revenue", "sum")
    ).reset_index()
    
    rfm_master["Recency"] = (max_date - rfm_master["Last_Purchase"]).dt.days
    rfm_master["Historical_CLV"] = rfm_master["Monetary"] * 3
    rfm_master = rfm_master.drop(columns=["Last_Purchase"])
    
    return countries, monthly_summary, seasonal_summary, product_summary, hourly_summary, daily_summary, rfm_master

try:
    countries, monthly_data, seasonal_data, product_data, hourly_data, daily_data, rfm_data = load_and_preaggregate_data()
except Exception as e:
    st.error("Heads up: We can't find 'online_retail_ii_clean.parquet'. Make sure it's saved in this exact folder.")
    st.stop()


# 2. Sidebar Filter Configuration
st.sidebar.header("Global Filters")
selected_country = st.sidebar.selectbox("Pick a Country / Market", countries)


# 3. INSTANT FILTER SUBSETTING (No recalculating over millions of rows!)
if selected_country == "All":
    sub_monthly = monthly_data.groupby("Order_Month").sum(numeric_only=True).reset_index()
    sub_seasonal = seasonal_data.groupby(["Month_Num", "Calendar_Month"], observed=False).sum(numeric_only=True).reset_index()
    sub_product = product_data.groupby("Description").sum(numeric_only=True).reset_index()
    sub_hourly = hourly_data.groupby("Hour").sum(numeric_only=True).reset_index()
    sub_daily = daily_data.groupby("Day_of_Week", observed=False).sum(numeric_only=True).reset_index()
    sub_rfm = rfm_data
else:
    sub_monthly = monthly_data[monthly_data["Country"] == selected_country]
    sub_seasonal = seasonal_data[seasonal_data["Country"] == selected_country]
    sub_product = product_data[product_data["Country"] == selected_country]
    sub_hourly = hourly_data[hourly_data["Country"] == selected_country]
    sub_daily = daily_data[daily_data["Country"] == selected_country]
    sub_rfm = rfm_data[rfm_data["Country"] == selected_country]


# --- Main Navigation Split ---
tab_sales, tab_operational, tab_customers = st.tabs([
    "📈 Sales & Product Performance", 
    "🕒 Operational & Micro-Time Patterns",
    "👥 Customer RFM & Lifetime Value"
])

# Global font definitions for cleaner graphics readability
PLOTLY_FONT_SETTING = dict(family="Arial, sans-serif", size=13, color="#222222")


# ==============================================================================
# TAB 1: Macro Sales & Product Performance
# ==============================================================================
with tab_sales:
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(label="TOTAL REVENUE", value=f"£{sub_monthly['Revenue'].sum():,.2f}")
    with col2:
        st.metric(label="TOTAL UNIQUE ORDERS", value=f"{sub_monthly['Orders'].sum():,}")
    with col3:
        st.metric(label="UNIQUE PRODUCTS SOLD", value=f"{len(sub_product):,}")

    st.markdown("---")

    st.subheader("Monthly Sales & Order Volume Trends")
    fig_trend = go.Figure()
    fig_trend.add_trace(go.Bar(x=sub_monthly["Order_Month"], y=sub_monthly["Orders"], name="Order Volume", yaxis="y2", marker_color="rgba(44, 160, 44, 0.25)"))
    fig_trend.add_trace(go.Scatter(x=sub_monthly["Order_Month"], y=sub_monthly["Revenue"], name="Revenue (£)", mode="lines+markers", line=dict(color="#1f77b4", width=3)))

    # FIXED: Replaced invalid dictionary properties with proper Plotly font syntax using weight="bold"
    fig_trend.update_layout(
        font=PLOTLY_FONT_SETTING,
        xaxis=dict(title="Timeline (Year-Month)", title_font=dict(size=14, weight="bold")),
        yaxis=dict(title="Total Revenue (£)", title_font=dict(color="#1f77b4", size=14, weight="bold"), tickfont=dict(color="#1f77b4", size=12)),
        yaxis2=dict(title="Unique Orders", title_font=dict(color="#2ca02c", size=14, weight="bold"), tickfont=dict(color="#2ca02c", size=12), overlaying="y", side="right"),
        legend=dict(x=0.02, y=0.95, font=dict(size=12)),
        hovermode="x unified",
        margin=dict(l=40, r=40, t=20, b=40)
    )
    st.plotly_chart(fig_trend, use_container_width=True)

    col_left, col_right = st.columns(2)
    with col_left:
        st.subheader("🍂 Seasonal Revenue Patterns")
        fig_seasonal = px.bar(sub_seasonal.sort_values("Month_Num"), x="Calendar_Month", y="Revenue", labels={"Revenue": "Revenue (£)", "Calendar_Month": "Month"}, color_discrete_sequence=["#ff7f0e"])
        fig_seasonal.update_layout(font=PLOTLY_FONT_SETTING, xaxis_title_font=dict(size=14), yaxis_title_font=dict(size=14))
        st.plotly_chart(fig_seasonal, use_container_width=True)

    with col_right:
        st.subheader("🚀 Top 10 Best-Selling Products")
        top_products = sub_product.sort_values("Quantity", ascending=False).head(10).sort_values("Quantity", ascending=True)
        fig_products = px.bar(top_products, x="Quantity", y="Description", orientation="h", labels={"Quantity": "Units Sold", "Description": "Product Name"}, color_discrete_sequence=["#1f77b4"])
        fig_products.update_layout(font=PLOTLY_FONT_SETTING, xaxis_title_font=dict(size=14), yaxis_title_font=dict(size=14))
        st.plotly_chart(fig_products, use_container_width=True)


# ==============================================================================
# TAB 2: Operational & Micro-Time Patterns
# ==============================================================================
with tab_operational:
    st.subheader("🕒 Operational Transaction Timing & Habits")
    col_hourly, col_daily = st.columns(2)
    
    with col_hourly:
        st.markdown("**Hourly Checkout Frequency (Time of Day)**")
        fig_hourly = px.line(sub_hourly.sort_values("Hour"), x="Hour", y="Orders", markers=True, labels={"Orders": "Orders Checked Out", "Hour": "Hour of Day (24h)"}, color_discrete_sequence=["#1f77b4"])
        fig_hourly.update_layout(font=PLOTLY_FONT_SETTING, xaxis=dict(tickmode="linear", tick0=0, dtick=1), xaxis_title_font=dict(size=14), yaxis_title_font=dict(size=14))
        st.plotly_chart(fig_hourly, use_container_width=True)
        
    with col_daily:
        st.markdown("**Weekly Checkout Frequency (Day of Week)**")
        days_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Sunday"]
        sub_daily["Day_of_Week"] = pd.Categorical(sub_daily["Day_of_Week"], categories=days_order, ordered=True)
        fig_daily = px.bar(sub_daily.sort_values("Day_of_Week"), x="Day_of_Week", y="Orders", labels={"Orders": "Orders Checked Out", "Day_of_Week": "Day of Week"}, color_discrete_sequence=["#2ca02c"])
        fig_daily.update_layout(font=PLOTLY_FONT_SETTING, xaxis_title_font=dict(size=14), yaxis_title_font=dict(size=14))
        st.plotly_chart(fig_daily, use_container_width=True)


# ==============================================================================
# TAB 3: Customer Analytics (RFM & CLV)
# ==============================================================================
with tab_customers:
    st.subheader("👥 Customer Behavior & Lifetime Value Distributions")
    if sub_rfm.empty:
        st.warning("No recorded customer tracking IDs found for this market selection. Try switching back to 'All'.")
    else:
        c1, c2, c3 = st.columns(3)
        with c1:
            st.metric(label="AVERAGE RECENCY", value=f"{sub_rfm['Recency'].mean():.1f} Days")
        with c2:
            st.metric(label="AVERAGE FREQUENCY", value=f"{sub_rfm['Frequency'].mean():.1f} Orders")
        with c3:
            st.metric(label="AVERAGE HISTORICAL CLV", value=f"£{sub_rfm['Historical_CLV'].mean():,.2f}")
            
        st.markdown("---")
        st.subheader("📊 Customer Behavior Distributions")
        col_r, col_f, col_m = st.columns(3)
        
        with col_r:
            st.markdown("**Recency Profile (Days since last purchase)**")
            fig_r = px.histogram(sub_rfm, x="Recency", nbins=30, color_discrete_sequence=["#1f77b4"])
            fig_r.update_layout(font=PLOTLY_FONT_SETTING, showlegend=False, xaxis_title="Days", yaxis_title="Customers Count")
            st.plotly_chart(fig_r, use_container_width=True)
            
        with col_f:
            st.markdown("**Frequency Profile (Unique orders placed)**")
            fig_f = px.histogram(sub_rfm, x="Frequency", nbins=30, color_discrete_sequence=["#2ca02c"])
            fig_f.update_layout(font=PLOTLY_FONT_SETTING, showlegend=False, xaxis_title="Orders Placed", yaxis_title="Customers Count")
            st.plotly_chart(fig_f, use_container_width=True)
            
        with col_m:
            st.markdown("**Customer Lifetime Value Profile (3-Year CLV, <95th Percentile)**")
            clv_limit = sub_rfm["Historical_CLV"].quantile(0.95)
            filtered_clv = sub_rfm[sub_rfm["Historical_CLV"] < clv_limit]
            fig_m = px.histogram(filtered_clv, x="Historical_CLV", nbins=30, color_discrete_sequence=["#ff7f0e"])
            fig_m.update_layout(font=PLOTLY_FONT_SETTING, showlegend=False, xaxis_title="Projected Value (£)", yaxis_title="Customers Count")
            st.plotly_chart(fig_m, use_container_width=True)