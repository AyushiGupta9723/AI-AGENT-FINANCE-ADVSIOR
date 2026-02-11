from agent.state import AgentState
from langchain_core.messages import HumanMessage
import re


def parse_money(value: str) -> int:
    """
    Convert money string like:
    90000
    90,000
    90k
    1.5l
    2 lakh
    into integer rupees
    """

    value = value.lower().replace(",", "").replace("₹", "").strip()

    # 90k
    if value.endswith("k"):
        return int(float(value[:-1]) * 1_000)

    # 1.5l or 1.5 lakh
    if value.endswith("l"):
        return int(float(value[:-1]) * 100_000)

    if "lakh" in value:
        number = re.findall(r"\d+\.?\d*", value)[0]
        return int(float(number) * 100_000)

    # default numeric
    return int(float(value))


def persist_user_profile(state: AgentState):
    profile = state.get("user_profile") or {}

    for msg in reversed(state["messages"]):
        if isinstance(msg, HumanMessage):
            text = msg.content.lower()

            # -------- AGE --------
            age_match = re.search(r"(\d{1,3})\s*(years?|yrs?)?\s*old", text)
            if age_match:
                profile["age"] = int(age_match.group(1))

            # -------- INCOME --------
            income_match = re.search(
                r"(earn|income).*?([\d.,]+k?|[\d.,]+l|[\d.,]+\s*lakh?)",
                text,
            )
            if income_match:
                profile["monthly_income"] = parse_money(
                    income_match.group(2)
                )

            # -------- EXPENSE --------
            expense_match = re.search(
                r"(spend|expense).*?([\d.,]+k?|[\d.,]+l|[\d.,]+\s*lakh?)",
                text,
            )
            if expense_match:
                profile["monthly_expenses"] = parse_money(
                    expense_match.group(2)
                )

            # -------- INCOME STABILITY --------
            if "stable income" in text:
                profile["income_stability"] = "stable"
            elif "unstable income" in text:
                profile["income_stability"] = "unstable"

            break

    if profile:
        return {"user_profile": profile}

    return {}
