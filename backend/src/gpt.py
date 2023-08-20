import os
import openai
from fastapi import FastAPI, HTTPException
from typing import List, Tuple

class Chat():
    def __init__(self) -> None:
        self.openai_key = os.getenv["OPENAI_KEY"]
        if not self.openai_key:
            raise HTTPException(status_code=404, detail="CHAVE OPENAI NULA")
        
    @staticmethod
    def _historic_format(historic: List[Tuple[str,str]]):
        _historic_format = []
        for msg in historic:
            _historic_format.append({ "role": "user", "content": msg[0]})
            _historic_format.append({ "role": "assistant", "content": msg[1]})
        return _historic_format
    
    def send(self, system_msg: str,  historic: List[Tuple[str,str]], message: str):
        self.messages.append({ "role": "user", "content": message })
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": system_msg},
                Chat._historic_format(historic)
            ]
        )
        message = response['choices'][0]['message']
        self.messages.append(message)
        return message['content']
