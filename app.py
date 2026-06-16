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

    if len(recurring) > 0:
        st.dataframe(recurring)
    else:
        st.warning("No recurring subscriptions found.")