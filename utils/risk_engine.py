import pandas as pd

def get_risk_level(score):
    if score >= 70:
        return "🔴 High"

    elif score >= 40:
        return "🟡 Medium"

    return "🟢 Low"


def calculate_risk(subscription_df):

    df = subscription_df.copy()

    total_monthly = df["Monthly_Cost"].sum()

    max_monthly = df["Monthly_Cost"].max()
    max_occurrence = df["Occurrences"].max()
    max_yearly = df["Yearly_Cost"].max()

    risk_scores = []

    for _, row in df.iterrows():

        monthly_score = row["Monthly_Cost"] / max_monthly

        yearly_score = row["Yearly_Cost"] / max_yearly

        occurrence_score = row["Occurrences"] / max_occurrence

        spending_score = row["Monthly_Cost"] / total_monthly

        risk = (
            monthly_score * 40
            + spending_score * 30
            + occurrence_score * 20
            + yearly_score * 10
        )

        risk_scores.append(round(risk))

    df["Risk Score"] = risk_scores

    df["Risk Level"] = (
        df["Risk Score"]
        .apply(get_risk_level)
    )

    return df