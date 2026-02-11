import streamlit as st
import requests
import uuid

# ---------------- CONFIG ----------------
API_BASE = "http://127.0.0.1:8000"
CHAT_STREAM_URL = f"{API_BASE}/chat/stream"
THREADS_URL = f"{API_BASE}/threads"
HISTORY_URL = f"{API_BASE}/history"

st.set_page_config(page_title="AI Finance Advisor", layout="centered")
st.title("💰 AI Finance Advisor")

# ---------------- UTILS ----------------
def generate_thread_id():
    return str(uuid.uuid4())


def stream_from_api(message, thread_id):
    with requests.post(
        CHAT_STREAM_URL,
        json={"message": message, "thread_id": thread_id},
        stream=True,
        timeout=120,
    ) as response:
        for line in response.iter_lines():
            if line:
                decoded = line.decode("utf-8")
                if decoded.startswith("data: "):
                    yield decoded.replace("data: ", "")


def load_threads():
    return requests.get(THREADS_URL, timeout=10).json()


def load_history(thread_id):
    return requests.get(f"{HISTORY_URL}/{thread_id}", timeout=10).json()


# ---------------- SESSION STATE ----------------
if "thread_id" not in st.session_state:
    st.session_state.thread_id = generate_thread_id()

if "messages" not in st.session_state:
    st.session_state.messages = []

if "threads" not in st.session_state:
    st.session_state.threads = load_threads()

# ---------------- SIDEBAR ----------------
st.sidebar.title("💬 Conversations")

if st.sidebar.button("➕ New Chat"):
    st.session_state.thread_id = generate_thread_id()
    st.session_state.messages = []
    st.session_state.threads.insert(0, st.session_state.thread_id)
    st.rerun()

# Thread selector
selected_thread = st.sidebar.radio(
    "Select a conversation",
    options=st.session_state.threads,
    index=(
        st.session_state.threads.index(st.session_state.thread_id)
        if st.session_state.thread_id in st.session_state.threads
        else 0
    )
)

# Load history on thread change
if selected_thread != st.session_state.thread_id:
    st.session_state.thread_id = selected_thread
    st.session_state.messages = load_history(selected_thread)
    st.rerun()

# ---------------- CHAT UI ----------------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

user_input = st.chat_input("Ask your finance question...")

if user_input:
    # user message
    st.session_state.messages.append(
        {"role": "user", "content": user_input}
    )
    with st.chat_message("user"):
        st.markdown(user_input)

    # assistant streaming
    with st.chat_message("assistant"):
        full_response = ""
        placeholder = st.empty()

        for token in stream_from_api(
            user_input,
            st.session_state.thread_id,
        ):
            full_response += token
            placeholder.markdown(full_response)

    st.session_state.messages = load_history(
    st.session_state.thread_id
    )

