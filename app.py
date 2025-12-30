# app.py
# ---------------------------------------------
# E-Commerce Analytics & Churn Intelligence Dashboard
# Designed for Executives & Retention Teams
# ---------------------------------------------

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------------------------------------
# Page Configuration
# ---------------------------------------------
st.set_page_config(
    page_title="E-Commerce Analytics Dashboard",
    layout="wide"
)

# ---------------------------------------------
# Load Data
# ---------------------------------------------
@st.cache_data
def load_data():
    return pd.read_csv("data/processed/dashboard_data.csv")

data = load_data()

# ---------------------------------------------
# Title
# ---------------------------------------------
st.title("📊 E-Commerce Analytics & Churn Intelligence Dashboard")
st.markdown("**Audience:** Executives & Marketing / Retention Teams")

# ---------------------------------------------
# Tabs
# ---------------------------------------------
tab1, tab2, tab3, tab4 = st.tabs([
    "📌 Executive Overview",
    "🧩 Customer Segments",
    "⚠️ Churn Risk Analysis",
    "🎯 Action Recommendations"
])

# =================================================
# TAB 1 — EXECUTIVE OVERVIEW
# =================================================
with tab1:
    st.subheader("Executive Overview")

    total_customers = data["customer_id"].nunique()
    churn_rate = data["actual_churn"].mean() * 100
    high_risk_pct = (data["risk_level"] == "High Risk").mean() * 100
    avg_clv = data["clv_proxy"].mean()

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Total Customers", total_customers)
    col2.metric("Churn Rate (%)", f"{churn_rate:.2f}")
    col3.metric("High-Risk Customers (%)", f"{high_risk_pct:.2f}")
    col4.metric("Average CLV", f"{avg_clv:.2f}")

    st.divider()

    # Churn Risk Distribution
    st.subheader("Churn Risk Distribution")

    risk_counts = data["risk_level"].value_counts()

    fig, ax = plt.subplots()
    ax.pie(
        risk_counts,
        labels=risk_counts.index,
        autopct="%1.1f%%",
        startangle=90
    )
    ax.axis("equal")
    st.pyplot(fig)

    # CLV Distribution
    st.subheader("Customer Lifetime Value Distribution")

    fig, ax = plt.subplots()
    ax.hist(data["clv_proxy"], bins=30)
    ax.set_xlabel("CLV")
    ax.set_ylabel("Number of Customers")
    st.pyplot(fig)

# =================================================
# TAB 2 — CUSTOMER SEGMENTS
# =================================================
with tab2:
    st.subheader("Customer Segment Insights")

    segment_summary = data.groupby("segment").agg(
        customers=("customer_id", "count"),
        avg_clv=("clv_proxy", "mean"),
        churn_rate=("actual_churn", "mean")
    ).reset_index()

    st.dataframe(segment_summary, use_container_width=True)

    st.subheader("Segment-wise Churn Rate")

    fig, ax = plt.subplots()
    ax.bar(
        segment_summary["segment"],
        segment_summary["churn_rate"]
    )
    ax.set_xlabel("Segment")
    ax.set_ylabel("Churn Rate")
    st.pyplot(fig)

# =================================================
# TAB 3 — CHURN RISK ANALYSIS (OPERATIONS)
# =================================================
with tab3:
    st.subheader("Customer Churn Risk Table")

    risk_filter = st.selectbox(
        "Filter by Risk Level",
        options=["All", "High Risk", "Medium Risk", "Low Risk"]
    )

    filtered_data = data.copy()
    if risk_filter != "All":
        filtered_data = filtered_data[
            filtered_data["risk_level"] == risk_filter
        ]

    st.dataframe(
        filtered_data[
            ["customer_id", "segment", "clv_proxy",
             "churn_probability", "risk_level"]
        ].sort_values("churn_probability", ascending=False),
        use_container_width=True
    )

# =================================================
# TAB 4 — ACTION RECOMMENDATIONS
# =================================================
with tab4:
    st.subheader("Retention Action Recommendations")

    st.markdown("""
    **Recommended Actions Based on Customer Risk & Value**
    
    - **High Risk + High CLV** → Immediate retention offers, personalized contact  
    - **High Risk + Low CLV** → Limited incentives or automated campaigns  
    - **Medium Risk** → Reminder emails, light discounts  
    - **Low Risk** → No action required, nurture normally
    """)

    st.subheader("High-Value & High-Risk Customers")

    priority_customers = data[
        (data["risk_level"] == "High Risk") &
        (data["clv_proxy"] > data["clv_proxy"].median())
    ]

    st.dataframe(
        priority_customers[
            ["customer_id", "segment", "clv_proxy", "churn_probability"]
        ].sort_values("churn_probability", ascending=False),
        use_container_width=True
    )
