import requests
import pytest

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

if __name__ == "__main__":
    pytest.main()