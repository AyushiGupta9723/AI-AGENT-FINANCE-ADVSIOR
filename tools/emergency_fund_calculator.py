from langchain.tools import tool

@tool
def emergency_fund_calculator(
    monthly_expenses: float,
    months: int = 6
) -> dict:
    """
    Calculate recommended emergency fund.
    """

    fund = monthly_expenses * months

    return {
        "monthly_expenses": monthly_expenses,
        "recommended_months": months,
        "emergency_fund_required": round(fund, 2)
    }
