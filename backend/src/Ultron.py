from database_handler import fetch_student_bio, insert_question, insert_answer
import os
from fastapi import FastAPI, HTTPException
from database_handler import SqlDatabase, Student
from gpt import Chat
from typing import List, Tuple
from pydantic import BaseModel
from sqlalchemy.orm import sessionmaker
from sqlalchemy import desc
from database_handler import Interaction
class ProcessQuestionResponse(BaseModel):
    status_code: int
    response: str
    error_message: str = None

class Ultron:
    historic_size = 2
    def __init__(self, uc: str):
        self.uc = uc
        self.questions_db = SqlDatabase('interactions')
        self.chat = Chat(uc)

    def _db_get_historic(self, student_id: str) -> List[Tuple[str, str]]:
        session = self.questions_db.get_Session()
        
        # Consulta os registros para o student_id e uc especificados
        historic_query = session.query(Interaction.pergunta, Interaction.resposta)\
            .filter_by(ra=student_id, uc=uc)\
            .order_by(desc(Interaction.timestamp))\
            .limit(size)

        # Converte os resultados em uma lista de tuplas
        historic = [(record.pergunta, record.resposta) for record in historic_query]
        return self.questions_db.get_historic(self.uc, student_id, self.historic_size)

    def _db_store(self, student_id: str, question: str, answer: str) -> bool:
        return self.questions_db.store_interaction(self.uc, student_id, question, answer)
    
    def _model_endpoint_check_question(self, question: str, uc: str) -> bool:
        # CONSULTA A PERGUNTA A UM MODELO DE SIMILARIDADE DO PROMPT/UC
        return True

    def _model_endpoint_get_answer(self,student_id: str, student_bio: str, question: str) -> str:
       historic = self._get_historic(student_id)
       return self.chat.send(system_msg = student_bio, historic = historic, message = question)
    
    def process_question(self, student_id: str, student_bio: str, question: str) -> ProcessQuestionResponse:

        # Verifica se a pergunta está de acordo com o conteúdo do LLM:
        if not self._model_endpoint_check_question(question):
            return ProcessQuestionResponse(status_code=400, error_message=f"Pergunta fora do escopo da uc {self.uc}")

        # Obtem do banco a lista de tuplas de pergunta,resposta
        try:
            historic = self._db_get_historic(student_id)
        except Exception as e:
            return ProcessQuestionResponse(status_code=503, error_message=f"Banco de dados está indisponível, traceback: {e}")

        # Obtem do LLM a pergunta,resposta
        try:
            response = self.chat.send(system_msg=student_bio, historic=historic, message=question)
        except Exception as e:
            return ProcessQuestionResponse(status_code=503, error_message=f"GPT está indisponível, traceback: {e}")

        # Armazenar a pergunta e resposta no banco
        try:
            success = self._insert_answer(student_id, question, response)
            if not success:
                raise Exception("Falha ao inserir resposta no banco de dados")
        except Exception as e:
            return ProcessQuestionResponse(status_code=503, error_message=f"Banco de dados está indisponível, traceback: {e}")

        return ProcessQuestionResponse(status_code=200, response=response)