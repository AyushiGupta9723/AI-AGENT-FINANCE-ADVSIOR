import os
from dotenv import load_dotenv

from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_community.vectorstores import FAISS

load_dotenv()

DATA_DIR = "rag/data"
VECTORSTORE_DIR = "rag/vectorstore/faiss_index"


# -------------------------------
# Domain keyword mapping
# -------------------------------
DOMAIN_KEYWORDS = {
    "mutual_funds": [
        "mutual fund", "equity fund", "debt fund", "hybrid fund", "nav"
    ],
    "taxation": [
        "tax", "80c", "elss", "ltcg", "stcg", "capital gains"
    ],
    "retirement": [
        "retirement", "pension", "corpus", "post-retirement"
    ],
    "risk_allocation": [
        "risk", "asset allocation", "equity allocation", "debt allocation"
    ],
    "sip_lumpsum": [
        "sip", "lump sum", "systematic investment"
    ],
}


def detect_domain(text: str) -> str:
    text_lower = text.lower()
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for kw in keywords:
            if kw in text_lower:
                return domain
    return "general"


# -------------------------------
# Load PDFs
# -------------------------------
def load_all_pdfs(data_dir: str):
    documents = []

    for filename in os.listdir(data_dir):
        if filename.lower().endswith(".pdf"):
            file_path = os.path.join(data_dir, filename)
            print(f"📄 Loading: {filename}")

            loader = PyPDFLoader(file_path)
            docs = loader.load()

            for doc in docs:
                doc.metadata["source"] = filename

            documents.extend(docs)

    return documents


# -------------------------------
# Ingestion Pipeline
# -------------------------------
def ingest():
    print("🔹 Loading PDFs...")
    raw_documents = load_all_pdfs(DATA_DIR)
    print(f"🔹 Total pages loaded: {len(raw_documents)}")

    print("🔹 Splitting into chunks...")
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=120
    )
    chunks = splitter.split_documents(raw_documents)
    print(f"🔹 Total chunks created: {len(chunks)}")

    print("🔹 Attaching domain metadata...")
    for chunk in chunks:
        chunk.metadata["domain"] = detect_domain(chunk.page_content)

    print("🔹 Creating embeddings & vector store...")
    embeddings = OpenAIEmbeddings(
        base_url="https://openrouter.ai/api/v1",
        model="text-embedding-3-small"
    )

    vectorstore = FAISS.from_documents(chunks, embeddings)

    os.makedirs(os.path.dirname(VECTORSTORE_DIR), exist_ok=True)
    vectorstore.save_local(VECTORSTORE_DIR)

    print("✅ RAG ingestion completed successfully")


if __name__ == "__main__":
    ingest()
