from bottle import Bottle, run, template

app = Bottle()

@app.route('/mainpage')
def mainPage():
    return template('Hello MainPageHTML Incoming')
    return template("mainpage.html")

run(app, host='localhost', port=8080, debug=True)
