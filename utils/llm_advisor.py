import os
from dotenv import load_dotenv
from google import genai

load_dotenv()


def generate_financial_advice(subscription_df):
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        return "Gemini API key not found. Please add GEMINI_API_KEY in your .env file."

    client = genai.Client(api_key=api_key)

    summary = subscription_df[
        [
            "Description",
            "Monthly_Cost",
            "Yearly_Cost",
            "Risk Score",
            "Risk Level",
            "Cancel Probability",
            "ML Prediction"
        ]
    ].to_string(index=False)

    prompt = f"""
You are an AI financial advisor.

Analyze this user's subscription spending:

{summary}

Give:
1. Overall summary
2. Highest risk subscription
3. Possible yearly savings
4. Three simple recommendations

Keep it under 200 words.
Do not give investment advice.
"""

    try:
        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=prompt
        )

        return response.text

    except Exception :
        high_risk = subscription_df.sort_values(
            by="Risk Score",
            ascending=False
         ).iloc[0]
        total_yearly = subscription_df["Yearly_Cost"].sum()
        return f"""
### AI Financial Advisor Fallback Report

Your total estimated yearly subscription spending is ₹{total_yearly:.0f}.

The highest-risk subscription is **{high_risk["Description"]}** with a risk score of **{high_risk["Risk Score"]}/100**.

Recommendations:

1. Review **{high_risk["Description"]}** first.
2. Cancel or pause subscriptions you rarely use.
3. Recheck recurring payments every month.

Possible yearly savings by reviewing the highest-risk subscription: ₹{high_risk["Yearly_Cost"]:.0f}.
"""            
        #return (
         #   "Gemini API Error:\n\n"
          #  f"{e}\n\n"
           # "This usually happens due to quota limit, invalid API key, or billing/project setup issue."
        #)