
from bottle import route, run, template, Bottle

app = Bottle()

@route('/hello')
def index(name):
    return "Hello World!"

run(app, host='localhost', port=8080)
