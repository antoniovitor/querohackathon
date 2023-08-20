from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from Ultron import Ultron
import os
import uvicorn
from Ultron import ProcessQuestionResponse

app = FastAPI()
PORT = int(os.getenv("PORT", 8000))
UC = os.getenv("UC")
ultron = Ultron(UC)

class ProcessQuestionRequest(BaseModel):
    student_id: str
    student_bio: str
    question: str

@app.get("/")
async def hello() -> str:
    msg="WELCOME TO ULTRON SERVICE, PLEASE ACESS /DOCS"
    return msg

@app.post("/ultron/process")
async def process_question(request: ProcessQuestionRequest) -> ProcessQuestionResponse:
    return ultron.process_question(
        request.student_id, request.student_bio, request.question
    )

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)