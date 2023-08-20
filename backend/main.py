import web
import gpt
from dotenv import load_dotenv

urls = (
    '/chat/(.*)', 'ChatEndpoint'
)
app = web.application(urls, globals())

class ChatEndpoint:
    def POST(self, hash):
        print(hash)
        return 'here'

        chat = gpt.Chat()
        message = chat.send('Who won the world series in 2020?')

if __name__ == "__main__":
    load_dotenv()
    app.run()