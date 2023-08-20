import requests
import pytest
from ..src.gpt import Chat

class Testchat:
    def test_chat_index(self):
        response = requests.get("http://localhost:8080/chat")
        assert response.status_code == 200
        assert type(response.content) == list
        chat = response.content[0]
        assert "id" in chat
        assert "hash" in chat

    def test_chat_creation(self):
        data = {"yuri", "vitor", "douglas"}
        response = requests.post("http://localhost:8080/chat/create", data=data)
        assert response.status_code == 200
        chat = response.content
        assert "id" in chat
        assert "hash" in chat

class TestGPA():
    def test_chatGPT_without_history():
        system_msg = 'You are a helpful assistant.'
        historic = []
        message = 'Who won the world series in 2020?'

        chat = Chat()
        chat.send(system_msg, historic, message)

    def test_chatGPT_with_history():
        system_msg = 'You are a helpful assistant.'
        historic = [
            ('Who won the world series in 2020?', 'The Los Angeles Dodgers won the World Series in 2020.'),
        ]
        message = 'Where was it played?'

        chat = Chat()
        chat.send(system_msg, historic, message)

if __name__ == "__main__":
    pytest.main()