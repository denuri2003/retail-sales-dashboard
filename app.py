import streamlit as st
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# ── Page config ──
st.set_page_config(
    page_title="Retail Sales Dashboard",
    page_icon="📊",
    layout="wide"
)

# ── Load data ──
engine = create_engine("sqlite:///data/sales.db")
df = pd.read_sql("SELECT * FROM orders", engine)
df["order_date"] = pd.to_datetime(df["order_date"])
df["year"] = df["order_date"].dt.year
df["month"] = df["order_date"].dt.to_period("M").astype(str)

# ── Sidebar filters ──
st.sidebar.title("Filters")
years = sorted(df["year"].unique())
selected_year = st.sidebar.selectbox("Select Year", ["All"] + years)
regions = sorted(df["region"].unique())
selected_regions = st.sidebar.multiselect("Select Region", regions, default=regions)

# ── Apply filters ──
filtered = df.copy()
if selected_year != "All":
    filtered = filtered[filtered["year"] == selected_year]
if selected_regions:
    filtered = filtered[filtered["region"].isin(selected_regions)]

# ── Title ──
st.title("Retail Sales Dashboard")
st.markdown("---")

# ── KPI Cards ──
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Revenue",    f"${filtered['sales'].sum():,.0f}")
col2.metric("Total Profit",     f"${filtered['profit'].sum():,.0f}")
col3.metric("Total Orders",     f"{len(filtered):,}")
col4.metric("Profit Margin",    f"{filtered['profit'].sum()/filtered['sales'].sum()*100:.1f}%")

st.markdown("---")

# ── Row 1: Monthly trend + Category donut ──
col1, col2 = st.columns([2, 1])

with col1:
    monthly = filtered.groupby("month")["sales"].sum().reset_index()
    fig1 = px.line(monthly, x="month", y="sales",
                   title="Monthly Revenue Trend",
                   labels={"sales": "Revenue ($)", "month": "Month"})
    fig1.update_traces(line_color="#378ADD", line_width=2)
    fig1.update_layout(xaxis_tickangle=-45)
    st.plotly_chart(fig1, use_container_width=True)

with col2:
    cat = filtered.groupby("category")["sales"].sum().reset_index()
    fig2 = px.pie(cat, values="sales", names="category",
                  title="Revenue by Category",
                  hole=0.4)
    st.plotly_chart(fig2, use_container_width=True)

# ── Row 2: Region bar + Profit by category ──
col1, col2 = st.columns(2)

with col1:
    region = filtered.groupby("region")["sales"].sum().reset_index().sort_values("sales", ascending=True)
    fig3 = px.bar(region, x="sales", y="region",
                  orientation="h",
                  title="Revenue by Region",
                  labels={"sales": "Revenue ($)", "region": "Region"},
                  color="sales", color_continuous_scale="Blues")
    st.plotly_chart(fig3, use_container_width=True)

with col2:
    profit_cat = filtered.groupby("category")[["sales","profit"]].sum().reset_index()
    profit_cat["margin"] = (profit_cat["profit"] / profit_cat["sales"] * 100).round(1)
    fig4 = px.bar(profit_cat, x="category", y="profit",
                  title="Profit by Category",
                  labels={"profit": "Profit ($)", "category": "Category"},
                  color="profit",
                  color_continuous_scale="Greens",
                  text="margin")
    fig4.update_traces(texttemplate="%{text}% margin", textposition="outside")
    st.plotly_chart(fig4, use_container_width=True)

# ── Row 3: Top products ──
st.subheader("Top 10 Products by Profit")
top_products = filtered.groupby("product_name")["profit"].sum().reset_index()
top_products = top_products.sort_values("profit", ascending=False).head(10)
fig5 = px.bar(top_products, x="profit", y="product_name",
              orientation="h",
              labels={"profit": "Profit ($)", "product_name": "Product"},
              color="profit", color_continuous_scale="teal")
fig5.update_layout(yaxis={"categoryorder": "total ascending"})
st.plotly_chart(fig5, use_container_width=True)

# ── Row 4: Raw data table ──
st.subheader("Raw Data")
st.dataframe(
    filtered[["order_date","region","category","product_name","sales","profit","quantity","discount"]]
    .sort_values("order_date", ascending=False)
    .head(100),
    use_container_width=True
)