import pandas as pd
from sklearn.ensemble import RandomForestClassifier


def train_model():
    data = pd.read_csv("data/training_data.csv")

    X = data[["Monthly_Cost", "Occurrences", "Yearly_Cost", "Risk_Score"]]
    y = data["Cancelled"]

    model = RandomForestClassifier(
        n_estimators=100,
        random_state=42
    )

    model.fit(X, y)

    return model


def predict_cancellation(model, subscription_df):
    X = subscription_df[[
        "Monthly_Cost",
        "Occurrences",
        "Yearly_Cost",
        "Risk Score"
    ]].copy()

    X = X.rename(columns={
        "Risk Score": "Risk_Score"
    })

    predictions = model.predict(X)
    probabilities = model.predict_proba(X)[:, 1]

    subscription_df["ML Prediction"] = [
        "Likely Review/Cancel" if pred == 1 else "Likely Keep"
        for pred in predictions
    ]

    subscription_df["Cancel Probability"] = [
        round(prob * 100) for prob in probabilities
    ]

    return subscription_df