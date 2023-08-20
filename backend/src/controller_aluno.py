from fastapi import FastAPI
from Aluno import Aluno
from fastapi import FastAPI
from pydantic import BaseModel
import uvicorn
import os

app = FastAPI()
PORT = int(os.getenv("PORT",8000))

def get_aluno(RA: str):
    return Aluno(RA)

class UpdateBioRequest(BaseModel):
    new_bio: str

class AskUltronRequest(BaseModel):
    question: str

class CadastrarAlunoRequest(BaseModel):
    RA: str
    bio: str

@app.get("/")
async def hello() -> str:
    msg="WELCOME TO ALUNO SERVICE, PLEASE ACESS /DOCS"
    return msg

@app.post("/aluno/{RA}/bio")
async def update_bio(RA: str, request: UpdateBioRequest):
    aluno = Aluno(RA)
    response = aluno.alterar_bio(request.new_bio)
    return response

@app.post("/aluno/{RA}/ask")
async def ask_ultron(RA: str, request: AskUltronRequest):
    aluno = Aluno(RA)
    response = aluno.ask_ultron(request.question)
    return response

@app.post("/aluno/cadastrar")
async def cadastrar_aluno(request: CadastrarAlunoRequest):
    return Aluno.db_cadastrar_aluno(request.RA, request.bio)

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=PORT)