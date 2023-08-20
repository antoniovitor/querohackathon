from database_handler import fetch_student_bio, insert_question, insert_answer

class Ultron:
    def __init__(self, openai_key, students_db_url, questions_db_url):
        self.openai_key = openai_key
        self.students_db_url = students_db_url
        self.questions_db_url = questions_db_url

    def llm_query(self, question, student_bio):
        # Simulação da chamada GPT-4
        # usar student_bio como system_msg
        # usar question como question
        # usar self.openai_key como openai_key
        return f"Resposta para '{question}' com biografia '{student_bio}'"
    
    def process_question(self, student_id, question):
        # Armazenar a pergunta no banco
        insert_question(self.questions_db_url, student_id, question)
        
        # Obter a biografia do aluno
        student_bio = fetch_student_bio(self.students_db_url, student_id)

        # Simular consulta ao GPT-4 com a pergunta e a biografia do aluno
        # No código real, você chamaria a API do GPT-4 aqui
        response = self.llm_query(question, student_bio)

        # Armazenar a resposta no banco
        insert_answer(self.questions_db_url, student_id, question, response)

        return response