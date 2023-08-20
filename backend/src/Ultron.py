from database_handler import fetch_student_bio, insert_question, insert_answer
import os
from fastapi import FastAPI, HTTPException
from database_handler import SqlDatabase, Student, 
from gpt import Chat
from typing import List, Tuple
class Ultron:
    def __init__(self):
        self.students_db = SqlDatabase('alunos')
        self.questions_db = SqlDatabase('interactions')
        self.chat = Chat()

    def _get_historic(self,ra,uc) -> List[Tuple[str,str]]:
        historic = []
        return historic

    def _check_question(self, question: str, uc: str) -> bool:
        # CONSULTA A PERGUNTA A UM MODELO DE SIMILARIDADE DO PROMPT/UC
        return True
    
    def _insert_answer(self, question: str, uc: str, ra: str) -> bool:
        # Armazenar a pergunta e resposta no banco
        return True
    
    def process_question(self, student_id: str, student_bio: str, question: str) -> str:

        # verifica se a pergunta está de acordo com a disciplina:
        if self.check_question(question):
        
            # Obtem do banco a lista de tuplas de pergunta,resposta
            # historic = self.get_historic(ra, uc)
            
            # Faz a pergunta com a bio do aluno
            # Simular consulta ao GPT-4 com a pergunta e a biografia do aluno
            # No código real, você chamaria a API do GPT-4 aqui
            #sponse = self.chat.send(system_msg = student_bio, historic = historic, message = question)

            # Armazenar a pergunta e resposta no banco
            #insert_answer(self.questions_db_url, student_id, question, response)

            #return response
            return "RESPOSTA : "
        else:
            return "PERGUNTA NAO ESTA DE ACORDO"