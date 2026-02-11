from langchain.tools import tool

@tool
def retirement_corpus_calculator(
    current_monthly_expense: float,
    current_age: int,
    retirement_age: int,
    inflation_rate: float = 6.0,
    post_retirement_years: int = 25
) -> dict:
    """
    Estimate required retirement corpus using inflation-adjusted expenses.

    Use when user asks about retirement planning or corpus calculation.
    """

    years_to_retirement = retirement_age - current_age

    future_annual_expense = (
        current_monthly_expense * 12 *
        ((1 + inflation_rate / 100) ** years_to_retirement)
    )

    required_corpus = future_annual_expense * post_retirement_years

    return {
        "current_age": current_age,
        "retirement_age": retirement_age,
        "future_annual_expense": round(future_annual_expense, 2),
        "required_retirement_corpus": round(required_corpus, 2),
        "assumed_inflation_rate": inflation_rate,
        "post_retirement_years": post_retirement_years
    }
