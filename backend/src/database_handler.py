from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import desc
import datetime
import os
from fastapi import FastAPI, HTTPException
from typing import List, Tuple
Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    bio = Column(String)

class Interaction(Base):
    __tablename__ = 'interactions'
    uc = Column(String, primary_key=True)
    ra = Column(String, primary_key=True)
    pergunta = Column(String)
    resposta = Column(String)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)

def init_db(db_url):
    engine = create_engine(db_url)
    Base.metadata.create_all(engine)

def fetch_student_bio(db_url, student_id):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    student = session.query(Student).filter_by(id=student_id).first()
    return student.bio if student else None

def insert_question(db_url, student_id, question):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    qa = Interaction(student_id=student_id, question=question)
    session.add(qa)
    session.commit()

def insert_answer(db_url, student_id, question, answer):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    qa = session.query(Interaction).filter_by(student_id=student_id, question=question).first()
    if qa:
        qa.answer = answer
        session.commit()

class SqlDatabase:
    _instance = None
    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(SqlDatabase, cls).__new__(cls)
            POSTGRES_URL = os.getenv('POSTGRES_URL')
            if not POSTGRES_URL:
                error_msg = F"ERRO EM VARIÁVEIS DE AMBIENTE POSTGRES_URL {POSTGRES_URL}"
                print(error_msg)
                raise HTTPException(status_code=404, detail=error_msg)
            #DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{db_name}'
            db_url = POSTGRES_URL + "/" + db_name
            print(f"trying to connecto on {db_url}")
            cls._instance.engine = create_engine(db_url)
        return cls._instance

    def get_engine(self):
        return self._instance.engine
    
    def get_Session(self) -> sessionmaker:
        return sessionmaker(bind=self.get_engine())
    
    # METODOS ULTRON
    def get_historic(self, uc: str, student_id: str, size: int) -> List[Tuple[str, str]]:
        

        return historic

    def store_interaction(self, uc: str, student_id: str, question: str, answer: str) -> bool:
        Session = sessionmaker(bind=self.get_engine())
        session = Session()

        # Cria o objeto Interaction com os valores fornecidos
        interaction = Interaction(uc=uc, ra=student_id, pergunta=question, resposta=answer, timestamp=datetime.datetime.utcnow())

        # Adiciona e confirma a transação
        session.add(interaction)
        session.commit()

        return True
    
    # METODOS ALUNO
    def get_student_by_ra(self, ra: str):
        Session = sessionmaker(bind=self.get_engine())
        session = Session()
        return session.query(Student).filter_by(id=ra).first()

    def update_student_bio(self, ra: str, new_bio: str):
        Session = sessionmaker(bind=self.get_engine())
        session = Session()
        student = session.query(Student).filter_by(id=ra).first()
        if student:
            student.bio = new_bio
            session.commit()

    def register_student(self, ra: str, bio: str):
        Session = sessionmaker(bind=self.get_engine())
        session = Session()
        existing_student = session.query(Student).filter_by(id=ra).first()
        if existing_student:
            raise HTTPException(status_code=400, detail="RA já cadastrado")
        new_student = Student(id=ra, bio=bio)
        session.add(new_student)
        session.commit()
