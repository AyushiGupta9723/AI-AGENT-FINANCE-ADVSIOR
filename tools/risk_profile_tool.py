from langchain.tools import tool

@tool

def risk_profile(
    age: int,
    income_stability: str,
    risk_tolerance: str
) -> dict:
    """
    Classify investor risk profile based on age and tolerance.
    """

    if age < 35 and risk_tolerance.lower() == "high":
        profile = "Aggressive"
    elif age < 50:
        profile = "Moderate"
    else:
        profile = "Conservative"

    return {
        "risk_profile": profile
    }
