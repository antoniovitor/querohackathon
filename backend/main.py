from fastapi import FastAPI
from Ultron import Ultron
from dotenv import load_dotenv
import os

load_dotenv()
app = FastAPI()

ultron = Ultron(openai_key=os.getenv("OPENAI_KEY"), students_db_url="URL_STUDENTS_DB", questions_db_url="URL_QUESTIONS_DB")

@app.post("/ask")
def ask_question(student_id: int, question: str):
    response = ultron.process_question(student_id, question)
    return {"response": response}