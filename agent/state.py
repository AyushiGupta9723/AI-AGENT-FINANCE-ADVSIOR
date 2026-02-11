from typing import Annotated, Optional, TypedDict, List
from langchain_core.messages import BaseMessage
from langgraph.graph.message import add_messages

class AgentState(TypedDict):
    messages: Annotated[List[BaseMessage], add_messages]
    user_profile: Optional[dict]
    risk_profile: Optional[str]