import os
import openai
from fastapi import FastAPI, HTTPException

class Chat():
    def __init__(self) -> None:
        self.openai_key = os.getenv["OPENAI_KEY"]
        if not self.openai_key:
            raise HTTPException(status_code=404, detail="CHAVE OPENAI NULA")
        self.messages = []
    
    def send(self, system_msg, message):
        self.messages.append({ "role": "user", "content": message })

        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                *self.messages
            ]
        )

        message = response['choices'][0]['message']
        self.messages.append(message)

        return message['content']
