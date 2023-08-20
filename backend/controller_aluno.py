from fastapi import FastAPI, Depends
from Aluno import Aluno

app = FastAPI()

def get_aluno(RA: str):
    return Aluno(RA)

@app.post("/aluno/{RA}/bio")
async def update_bio(new_bio: str, aluno: Aluno = Depends(get_aluno)):
    return aluno.alterar_bio(new_bio)

@app.post("/aluno/{RA}/ask")
async def ask_ultron(question: str, aluno: Aluno = Depends(get_aluno)):
    return aluno.ask_ultron(question)