from agent.state import AgentState
from langchain_core.messages import SystemMessage, AIMessage
from typing import Dict, Any


def make_agent_node(llm, base_system_message):
    def agent_node(state: AgentState) -> Dict[str, Any]:
        messages = [
            m for m in state["messages"]
            if not (isinstance(m, AIMessage) and m.content.strip().startswith("{"))
            ]


        system_parts = [base_system_message.content]

        # Inject known user profile
        if state.get("user_profile"):
            system_parts.append(
                f"Known user profile: {state['user_profile']}"
            )

        # Inject known risk profile
        if state.get("risk_profile"):
            system_parts.append(
                f"Known risk profile: {state['risk_profile']}"
            )

        system_message = SystemMessage(
            content="\n".join(system_parts)
        )

        if system_message not in messages:
            messages = [system_message] + messages

        response = llm.invoke(messages)
        return {"messages": [response]}

    return agent_node
