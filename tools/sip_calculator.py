from langchain_core.tools import tool
@tool
def sip_calculator(
        monthly_investment: float,
        years: float,
        expected_annual_return: float
        ) -> dict:
    """    Calculate the future value of a Systematic Investment Plan (SIP).
    Args:
        monthly_investment (float): The amount invested monthly.
        year (float): The number of years the investment will be made.
        expected_annual_return (float): The expected annual return rate (in percentage).
    Returns:
        dict: A dictionary containing the future value of the SIP and the total amount invested.
    
    Use when user asks about the sip, monthly investment, or long term investment growth.

    """
    r=expected_annual_return / 100 / 12  # Monthly return rate
    n=years * 12  # Total number of months
    future_value = monthly_investment * (((1 + r) ** n - 1) / r) * (1 + r)  # Future value of SIP
    return {
        "monthly_investment": monthly_investment,
        "years": years,
        "expected_annual_return": expected_annual_return,
        "future_value": future_value,
    }

