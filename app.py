import streamlit as st
import pandas as pd

st.title("💳 Subscription Waste Detector AI")

uploaded_file = st.file_uploader(
    "Upload Bank Statement CSV",
    type=["csv"]
)

if uploaded_file:

    df = pd.read_csv(uploaded_file)

    st.subheader("Uploaded Data")
    st.dataframe(df)

    recurring = (
        df.groupby("Description")
        .size()
        .reset_index(name="Occurrences")
    )

    recurring = recurring[recurring["Occurrences"] >= 2]

    st.subheader("Detected Recurring Subscriptions")
    st.dataframe(recurring)

    # Cost analysis MUST be inside this block
    subscription_cost = (
        df.groupby("Description")["Amount"]
        .mean()
        .abs()
        .reset_index()
    )

    subscription_cost = subscription_cost[
        subscription_cost["Description"].isin(recurring["Description"])
    ]

    subscription_cost["Yearly Cost"] = (
        subscription_cost["Amount"] * 12
    )

    #st.subheader("💰 Subscription Cost Analysis")
    #st.dataframe(subscription_cost)

    st.subheader("💰 Subscription Cost Analysis")
    st.dataframe(subscription_cost)

    monthly_cost = subscription_cost["Amount"].sum()
    yearly_cost = subscription_cost["Yearly Cost"].sum()

    col1, col2 = st.columns(2)

    with col1:
        st.metric(
            "Monthly Subscription Cost",
            f"₹{monthly_cost:.0f}"
        )

    with col2:
        st.metric(
            "Yearly Subscription Cost",
            f"₹{yearly_cost:.0f}"
        )
        st.subheader("🤖 AI Savings Recommendations")

    for _, row in subscription_cost.iterrows():
        name = row["Description"]
        monthly = row["Amount"]
        yearly = row["Yearly Cost"]

        if monthly >= 1000:
            risk = "🔴 High Cost"
            suggestion = "Review this subscription. It has a high yearly impact."
        elif monthly >= 500:
            risk = "🟡 Medium Cost"
            suggestion = "Keep only if you use it regularly."
        else:
            risk = "🟢 Low Cost"
            suggestion = "Low cost, but still review if unused."

        st.write(f"### {name}")
        st.write(f"Monthly Cost: ₹{monthly:.0f}")
        st.write(f"Yearly Cost: ₹{yearly:.0f}")
        st.write(f"Risk Level: {risk}")
        st.info(suggestion)    

