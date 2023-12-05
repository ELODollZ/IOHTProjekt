#!/usr/bin/env python3
# Author: NyboMønster

#Imports
from flask import Flask, render_template
from flask_socketio import SocketIO, emit


#Variables
app = Flask(__name__)
socketio = SocketIO(app)

###Routes
#the main socketio that emites to the webpage
@socketio.on('patientData')
def PatientData():
    Data = 0
    socketio.emit('PD', Data)


# Main Route
@app.route('/')
def indexHTML():
    return render_template('index.html')


#Host webpage onto network
if __name__ == '__main__':
    socketio.run(app, host="192.168.29.01", debug=True)

