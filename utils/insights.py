def generate_insight(row):

    if row["Risk Score"] >= 70:
        return (
            "This subscription contributes significantly to your recurring spending. "
            "Review whether you actively use it every month."
        )

    elif row["Risk Score"] >= 40:
        return (
            "Moderate recurring cost. Review usage occasionally to ensure it still provides value."
        )

    return (
        "Low financial impact. No immediate action required."
    )