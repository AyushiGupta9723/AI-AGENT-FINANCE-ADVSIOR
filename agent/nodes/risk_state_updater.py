from agent.state import AgentState
from langchain_core.messages import ToolMessage
import json
import re


def persist_risk_profile(state: AgentState):

    for msg in reversed(state["messages"]):

        if isinstance(msg, ToolMessage) and msg.name == "risk_profile":

            content = msg.content
            if not content:
                break

            # -------- Try JSON --------
            try:
                data = json.loads(content)
                risk = data.get("risk_profile")
                if risk:
                    return {"risk_profile": risk.lower()}
            except Exception:
                pass

            # -------- Fallback: Plain text extraction --------
            match = re.search(
                r"(conservative|moderate|aggressive)",
                content.lower()
            )
            if match:
                return {"risk_profile": match.group(1)}

        if not isinstance(msg, ToolMessage):
            break

    return {}
