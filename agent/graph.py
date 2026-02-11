from langgraph.graph import StateGraph
from langgraph.prebuilt import ToolNode, tools_condition

from agent.state import AgentState
from agent.nodes.agent_node import make_agent_node
from agent.nodes.risk_state_updater import persist_risk_profile
from agent.nodes.user_profile_state_updater import persist_user_profile
from llm.llm_provider import get_llm_with_tools,tools
from memory.checkpointer import get_checkpointer
from rag.retriever import finance_rag_tool

llm, system_message = get_llm_with_tools()
agent_node = make_agent_node(llm, system_message)

tool_node = ToolNode(tools)

graph = StateGraph(AgentState)

graph.add_node("agent", agent_node)
graph.add_node("tools", tool_node)
graph.add_node("persist_user", persist_user_profile)
graph.add_node("persist_risk", persist_risk_profile)

graph.set_entry_point("persist_user")
graph.add_edge("persist_user", "agent")
graph.add_conditional_edges(
    "agent",
    tools_condition,
    {
        "tools": "tools",
        "__end__": "__end__"
    }
)

graph.add_edge("tools", "persist_risk")
graph.add_edge("persist_risk", "agent")

checkpointer = get_checkpointer()

finance_agent = graph.compile(checkpointer=checkpointer)

def retrieve_all_threads():
    all_threads = set()
    for checkpoint in checkpointer.list(None):
        all_threads.add(checkpoint.config['configurable']['thread_id'])

    return list(all_threads)