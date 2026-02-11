from langchain.tools import tool

@tool
def emi_calculator(
    principal: float,
    annual_interest_rate: float,
    tenure_years: int
) -> dict:
    """
    Calculate EMI for a loan.
    Use when user asks about loan affordability or EMI.
    """

    r = annual_interest_rate / 100 / 12
    n = tenure_years * 12

    emi = principal * r * (1 + r)**n / ((1 + r)**n - 1)

    return {
        "loan_amount": principal,
        "annual_interest_rate": annual_interest_rate,
        "tenure_years": tenure_years,
        "monthly_emi": round(emi, 2)
    }
