from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from parser import parse_log
from llm_agent import ask_llm_with_memory
from utils import detect_anomalies, get_flight_time
from typing import Optional
import uvicorn
import uuid
import os

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

SESSION_CONTEXT = {}

class AskRequest(BaseModel):
    session_id: Optional[str] = None
    question: str
    log_id: str = "log171.bin"

@app.post("/ask")
async def ask_question(body: AskRequest):
    try:
        session_id = body.session_id or str(uuid.uuid4())

        log_path = f"logs/{body.log_id}"
        if not os.path.exists(log_path):
            return {"error": f"Log file '{body.log_id}' not found. Please upload it first."}

        df = parse_log(log_path)

        question_lower = body.question.lower()
        if "flight time" in question_lower:
            context = get_flight_time(df)
        elif "anomal" in question_lower or "issue" in question_lower:
            context = detect_anomalies(df)
        else:
            important_cols = ['TimeUS', 'Alt', 'GPS', 'Curr', 'Temp', 'Err', 'Mode']
            available_cols = [col for col in important_cols if col in df.columns]
            summary_df = df[available_cols].dropna().head(100)
            context = summary_df.to_string(index=False)

        past_messages = SESSION_CONTEXT.get(session_id, [])
        past_messages.append({"role": "user", "content": body.question})
        past_messages.append({"role": "system", "content": f"Flight context:\n{context}"})

        messages = [{"role": "system", "content": "You are a helpful UAV flight assistant."}] + past_messages
        answer = ask_llm_with_memory(messages)

        past_messages.append({"role": "assistant", "content": answer})
        SESSION_CONTEXT[session_id] = past_messages

        return {
            "session_id": session_id,
            "answer": answer
        }

    except Exception as e:
        return {"error": str(e)}

@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    file_path = f"logs/{file.filename}"
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return {"message": "File uploaded successfully", "filename": file.filename}

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)