from langchain_openai import ChatOpenAI
from langchain_core.messages import SystemMessage
from dotenv import load_dotenv

from llm.prompts import SYSTEM_PROMPT

from tools.sip_calculator import sip_calculator
from tools.retirement_calculator import retirement_corpus_calculator
from tools.emi_calculator import emi_calculator
from tools.emergency_fund_calculator import emergency_fund_calculator
from tools.asset_allocation_tool import asset_allocation
from tools.risk_profile_tool import risk_profile

from rag.retriever import finance_rag_tool

load_dotenv()
tools = [
    sip_calculator,
    retirement_corpus_calculator,
    emi_calculator,
    emergency_fund_calculator,
    asset_allocation,
    risk_profile,
    finance_rag_tool
]

def get_llm_with_tools():
    llm = ChatOpenAI(
        base_url="https://openrouter.ai/api/v1",
        model="openai/gpt-4o-mini",
        temperature=0,
        max_tokens=512,
        streaming=True,
    )


    return llm.bind_tools(tools), SystemMessage(content=SYSTEM_PROMPT)
