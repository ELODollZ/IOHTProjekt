#!/usr/bin/env python3
# Author: NyboMønster

#Imports
import sys
sys.path.insert(0, '/home/Gruppe2PI/Projekts/IOHTProjekt/Scripts')
from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from ConfigFile import ListOfConfig as Conf
from PatientIndexing import DataBaseControl
from threading import Thread


#Variables
app = Flask(__name__)
socketio = SocketIO(app)
###Routes
#the main socketio that emites to the webpage
@socketio.on('patientData')
def PatientData():
    #DBC = DataBaseControl(Conf[0], Conf[1], Conf[2])
    #ThreadDBC = Thread(target=DBC, args=[1])
    Data = ["2", "1", "4", "5", "10"]
    socketio.emit('PD', Data)

# Main Route
@app.route('/')
def indexHTML():
    return render_template('index.html')


#Host webpage onto network
if __name__ == '__main__':
    socketio.run(app, host="192.168.29.01", debug=True)

