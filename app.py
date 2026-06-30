import streamlit as st
import pandas as pd
import plotly.express as px
from utils.risk_engine import calculate_risk
from utils.insights import generate_insight
from models.util.ml_model import train_model, predict_cancellation
st.set_page_config(
    page_title="Subscription Waste Detector AI",
    page_icon="💳",
    layout="wide"
)

st.title("💳 Subscription Waste Detector AI")
st.write("Detect recurring subscriptions and estimate monthly/yearly waste.")

uploaded_file = st.file_uploader("Upload Bank Statement CSV", type=["csv"])

if uploaded_file:
    df = pd.read_csv(uploaded_file)

    df["Amount"] = pd.to_numeric(df["Amount"])
    expenses = df[df["Amount"] < 0].copy()
    expenses["Amount"] = expenses["Amount"].abs()

    recurring = (
        expenses.groupby("Description")
        .agg(
            Occurrences=("Description", "count"),
            Monthly_Cost=("Amount", "mean"),
            Total_Spent=("Amount", "sum")
        )
        .reset_index()
    )

    recurring = recurring[recurring["Occurrences"] >= 2]
    recurring["Yearly_Cost"] = recurring["Monthly_Cost"] * 12
    recurring = recurring.sort_values(by="Yearly_Cost", ascending=False)
    recurring = calculate_risk(recurring)
    model = train_model()
    recurring = predict_cancellation(model, recurring)
    high_risk_count = len(recurring[recurring["Risk Level"] == "🔴 High"])
    medium_risk_count = len(recurring[recurring["Risk Level"] == "🟡 Medium"])
    low_risk_count = len(recurring[recurring["Risk Level"] == "🟢 Low"])

    st.subheader("🤖 AI Risk Summary")

    col1, col2, col3 = st.columns(3)

    col1.metric("High Risk", high_risk_count)
    col2.metric("Medium Risk", medium_risk_count)
    col3.metric("Low Risk", low_risk_count)
    high_risk_subscriptions = recurring[recurring["Risk Level"] == "🔴 High"]
    potential_yearly_savings = high_risk_subscriptions["Yearly_Cost"].sum()
    st.metric(
        "Potential Yearly Savings",f"₹{potential_yearly_savings:.0f}"
    )
    

    st.subheader("📊 Dashboard")

    total_monthly = recurring["Monthly_Cost"].sum()
    total_yearly = recurring["Yearly_Cost"].sum()
    total_subscriptions = len(recurring)
    most_expensive = recurring.iloc[0]["Description"] if total_subscriptions > 0 else "None"

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Monthly Cost", f"₹{total_monthly:.0f}")
    col2.metric("Yearly Cost", f"₹{total_yearly:.0f}")
    col3.metric("Subscriptions", total_subscriptions)
    col4.metric("Most Expensive", most_expensive)

    st.subheader("🔁 Detected Subscriptions")
    st.dataframe(recurring)

    st.subheader("📈 Spending Charts")

    chart1 = px.pie(
        recurring,
        values="Monthly_Cost",
        names="Description",
        title="Monthly Subscription Share"
    )
    st.plotly_chart(chart1, use_container_width=True)

    chart2 = px.bar(
        recurring,
        x="Description",
        y="Yearly_Cost",
        title="Estimated Yearly Cost by Subscription"
    )
    st.plotly_chart(chart2, use_container_width=True)
    st.subheader("🤖 AI Financial Advisor")

    for _, row in recurring.iterrows():

        with st.expander(f"{row['Description']} ({row['Risk Level']})"):

           st.write(f"**Risk Score:** {row['Risk Score']}/100")
           st.write(generate_insight(row))
    st.subheader("🧠 Machine Learning Predictions")
    for _, row in recurring.iterrows():
        st.write(
            f"**{row['Description']}** → {row['ML Prediction']} "
            f"({row['Cancel Probability']}% probability)"
        )    
else:
    st.info("Upload a CSV file to start analysis.")