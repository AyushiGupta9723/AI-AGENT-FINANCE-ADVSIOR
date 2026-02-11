from langchain.tools import tool

@tool
def asset_allocation(
    age: int,
    risk_profile: str
) -> dict:
    """
    Suggest asset allocation based on age and risk profile.
    """

    risk_profile = risk_profile.capitalize()  

    equity = max(100 - age, 40)

    if risk_profile == "Aggressive":
        equity += 10
    elif risk_profile == "Conservative":
        equity -= 10

    equity = min(max(equity, 30), 80)
    debt = 100 - equity

    return {
        "equity_percent": equity,
        "debt_percent": debt
    }
