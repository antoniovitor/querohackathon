from fastapi import FastAPI, HTTPException
from sqlalchemy.orm import sessionmaker
from database_handler import SqlDatabase, Student
import os
from pydantic import BaseModel
import requests

class AlterarBioResponse(BaseModel):
    status: str
    new_bio: str

class AskUltronResponse(BaseModel):
    status: str
    msg: str

class CadastrarAlunoResponse(BaseModel):
    status: str
    RA: str

class Aluno:
    def __init__(self, RA: str):
        self.RA = RA
        self.sql_db = SqlDatabase('students')
        self.student_data = self.sql_db.get_student_by_ra(self.RA)
        if not self.student_data:
            raise HTTPException(status_code=404, detail="Aluno não cadastrado")
        self.bio = self.student_data.bio
        self.ULTRON_URL = os.getenv('ULTRON_URL')

    ### METODOS FASTAPI
    def db_alterar_bio(self, new_bio: str) -> AlterarBioResponse:
        self.sql_db.update_student_bio(self.RA, new_bio)
        return AlterarBioResponse(status="success", new_bio=new_bio)

    def model_endpoint_ask_ultron(self, question: str) -> AskUltronResponse:
        payload = {
            "question" : question,
            "ra" : self.RA,
            "bio" : self.bio
        }
        url = self.ULTRON_URL + "/ask"
        response = requests.post(url, payload)
        return AskUltronResponse(status="success", msg=response)
    
    @staticmethod
    def db_cadastrar_aluno(RA: str, bio: str) -> CadastrarAlunoResponse:
        sql_db = SqlDatabase('students')
        sql_db.register_student(RA, bio)
        return CadastrarAlunoResponse(status="success", RA=RA)