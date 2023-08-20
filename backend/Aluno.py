from fastapi import FastAPI, HTTPException
from databases import Database
import os

DB_URL = os.getenv('DBURL')
ULTRON_URL = os.getenv('ULTRON_URL')
database = Database(DB_URL)

app = FastAPI()

class Aluno:
    def __init__(self, RA: str):
        self.RA = RA
        self.student_data = self._get_student_by_ra()
        if not self.student_data:
            raise HTTPException(status_code=404, detail="Aluno não cadastrado")
        self.bio = self.student_data['bio']
        
    def _get_student_by_ra(self):
        # Considerando que a tabela 'students' contém os campos 'RA' e 'bio'
        query = f"SELECT * FROM students WHERE RA = {self.RA}"
        return database.fetch_one(query=query)

    def alterar_bio(self, new_bio: str):
        query = f"UPDATE students SET bio = {new_bio} WHERE RA = {self.RA}"
        database.execute(query=query)
        self.bio = new_bio

    def ask_ultron(self, question: str):
        # Implementar a lógica de comunicação com o endpoint Ultron
        pass

@app.post("/aluno/{RA}/bio")
async def update_bio(RA: str, new_bio: str):
    aluno = Aluno(RA)
    aluno.alterar_bio(new_bio)
    return {"status": "success"}

@app.post("/aluno/{RA}/ask")
async def ask_ultron(RA: str, question: str):
    aluno = Aluno(RA)
    aluno.ask_ultron(question)
    return {"status": "success"}
