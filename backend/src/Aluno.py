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
        self.sql_db = SqlDatabase('alunos')
        self.student_data = self._get_student_by_ra()
        if not self.student_data:
            raise HTTPException(status_code=404, detail="Aluno não cadastrado")
        self.bio = self.student_data.bio
        self.ULTRON_URL = os.getenv('ULTRON_URL')

    def _get_student_by_ra(self):
        Session = sessionmaker(bind=self.sql_db.get_engine())
        session = Session()
        return session.query(Student).filter_by(id=self.RA).first()

    ### METODOS FASTAPI
    def alterar_bio(self, new_bio: str) -> AlterarBioResponse:
        Session = sessionmaker(bind=self.sql_db.get_engine())
        session = Session()
        student = session.query(Student).filter_by(id=self.RA).first()
        if student:
            student.bio = new_bio
            session.commit()
        return AlterarBioResponse(status="success", new_bio=new_bio)

    def ask_ultron(self, question: str) -> AskUltronResponse:
        payload = {
            "question" : question,
            "ra" : self.RA
        }
        url = self.ULTRON_URL + "/ask"
        response = requests.post(url, payload)
        return AskUltronResponse(status="success", msg=response)
    
    @staticmethod
    def cadastrar_aluno(RA: str, bio: str) -> CadastrarAlunoResponse:
        sql_db = SqlDatabase('alunos')
        Session = sessionmaker(bind=sql_db.get_engine())
        session = Session()
        existing_student = session.query(Student).filter_by(id=RA).first()

        if existing_student:
            raise HTTPException(status_code=400, detail="RA já cadastrado")

        new_student = Student(id=RA, bio=bio)
        session.add(new_student)
        session.commit()
        return CadastrarAlunoResponse(status="success", RA=RA)
    ###