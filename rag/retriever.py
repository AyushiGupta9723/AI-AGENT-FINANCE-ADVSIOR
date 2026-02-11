from langchain.tools import tool
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

VECTORSTORE_DIR = "rag/vectorstore/faiss_index"

DOMAIN_HINTS = {
    "tax": "taxation",
    "elss": "taxation",
    "sip": "sip_lumpsum",
    "lump": "sip_lumpsum",
    "retire": "retirement",
    "allocation": "risk_allocation",
    "mutual": "mutual_funds"
}

def infer_domain(query: str):
    q = query.lower()
    for key, domain in DOMAIN_HINTS.items():
        if key in q:
            return domain
    return None

embeddings = OpenAIEmbeddings(
    base_url="https://openrouter.ai/api/v1",
    model="text-embedding-3-small",
)

vectorstore = FAISS.load_local(
    VECTORSTORE_DIR,
    embeddings,
    allow_dangerous_deserialization=True
)

@tool
def finance_rag_tool(query: str) -> str:
    """
    Retrieve authoritative explanations related to:
    - mutual fund categories
    - Indian tax rules (80C, ELSS, LTCG, STCG)
    - asset allocation strategies
    - retirement planning heuristics
    - SIP vs lump-sum investing
    - investing do’s and don’ts

    Use ONLY when the user explicitly asks for explanations or background.
    """
    domain = infer_domain(query)

    if domain:
        docs = vectorstore.similarity_search(
            query,
            k=4,
            filter={"domain": domain}
        )
    else:
        docs = vectorstore.similarity_search(query, k=4)

    combined_context = "\n\n".join(
        d.page_content for d in docs
    )

    return combined_context