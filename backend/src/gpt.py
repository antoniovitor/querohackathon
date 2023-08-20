import os
import openai

class Chat():
    def __init__(self) -> None:
        openai.api_key = os.getenv("OPENAI_KEY")
        self.messages = []
    
    def send(self, message):
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
