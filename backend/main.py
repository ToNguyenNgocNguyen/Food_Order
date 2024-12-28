from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from agent import graph, memory
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from fastapi.responses import StreamingResponse


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Replace '*' with your frontend's domain for better security
    allow_credentials=True,
    allow_methods=["POST"],  # Allow all HTTP methods, including OPTIONS
    allow_headers=["*"],  # Allow all headers
)

chat_history = {}

class ChatRequest(BaseModel):
    message: str
    thread_id: str
    customer_name: str


async def event_stream(request: ChatRequest):
    # Stream the response
    async for msg, metadata in graph.astream(
        {
            "messages": request.message
        },
        config={"configurable": {"thread_id": request.thread_id, 'customer_name': request.customer_name}}, stream_mode="messages"
    ):
        if msg.content and not isinstance(msg, HumanMessage) and metadata["langgraph_node"] == "assistant":
            # Yield the message content as an SSE event
            yield f"{msg.content}"


@app.post("/api/chat")
async def chat(request: ChatRequest):

    return StreamingResponse(event_stream(request))

# uvicorn main:app --reload --host 0.0.0.0 --port 5000
