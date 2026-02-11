from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from langchain_core.messages import HumanMessage, AIMessage
from agent.graph import finance_agent, checkpointer
from fastapi import HTTPException
import psycopg
import os

app = FastAPI(title="AI Finance Advisor API")


# -------------------- MODELS --------------------

class ChatRequest(BaseModel):
    message: str
    thread_id: str

# -------------------- STREAM CHAT --------------------
@app.post("/chat/stream")
def chat_stream(req: ChatRequest):

    def event_generator():
        try:
            config = {
                "configurable": {
                    "thread_id": req.thread_id,
                },
                "metadata": {
                    "thread_id": req.thread_id,
                    "source": "streamlit",
                    "app": "ai-finance-advisor",
                },
                "run_name": "chat_turn",
            }

            for message_chunk, _ in finance_agent.stream(
                {"messages": [HumanMessage(content=req.message)]},
                config=config,
                stream_mode="messages",
            ):
                if isinstance(message_chunk, AIMessage):
                    yield f"data: {message_chunk.content}\n\n"

        except Exception as e:
            error_msg = f"[ERROR] {type(e).__name__}: {str(e)}"
            yield f"data: {error_msg}\n\n"

        finally:
            yield "event: end\n\n"

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream",
    )


# -------------------- LIST THREADS --------------------

@app.get("/threads")
def list_threads():
    threads = set()
    for checkpoint in checkpointer.list(None):
        threads.add(checkpoint.config["configurable"]["thread_id"])
    return list(threads)


# -------------------- LOAD HISTORY --------------------

@app.get("/history/{thread_id}")
def get_history(thread_id: str):
    state = finance_agent.get_state(
        config={"configurable": {"thread_id": thread_id}}
    )

    messages = state.values.get("messages", [])

    history = []
    for msg in messages:
            if isinstance(msg, HumanMessage):
                history.append({
                    "role": "user",
                    "content": msg.content
                    }
                )
            elif isinstance(msg, AIMessage):
                history.append({
                    "role": "assistant",
                    "content": msg.content}
                    )

    return history

