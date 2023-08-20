from sqlalchemy import create_engine, Column, Integer, String, DateTime
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import datetime
import os

Base = declarative_base()

class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    bio = Column(String)

class QuestionAnswer(Base):
    __tablename__ = 'questions_answers'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer)
    question = Column(String)
    answer = Column(String)
    datetime = Column(DateTime, default=datetime.datetime.utcnow)

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
    qa = QuestionAnswer(student_id=student_id, question=question)
    session.add(qa)
    session.commit()

def insert_answer(db_url, student_id, question, answer):
    engine = create_engine(db_url)
    Session = sessionmaker(bind=engine)
    session = Session()
    qa = session.query(QuestionAnswer).filter_by(student_id=student_id, question=question).first()
    if qa:
        qa.answer = answer
        session.commit()

class SqlDatabase:
    _instance = None
    def __new__(cls, db_name):
        if cls._instance is None:
            cls._instance = super(SqlDatabase, cls).__new__(cls)
            POSTGRES_URL = os.getenv('POSTGRES_URL')
            POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')
            POSTGRES_USER = os.getenv('POSTGRES_USER')
            DB_URL = f'postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_URL}/{db_name}'
            cls._instance.engine = create_engine(DB_URL)
        return cls._instance

    def get_engine(self):
        return self._instance.engine
