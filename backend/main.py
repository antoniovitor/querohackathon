import web

urls = (
    '/(.*)', 'hello'
)
app = web.application(urls, globals())

class chat:
    def GET(self, hash):
        print(hash)

if __name__ == "__main__":
    app.run()