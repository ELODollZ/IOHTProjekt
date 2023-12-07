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
def PatientData(Data):
    #print(Data)
    Data = "Testing"
    socketio.emit('PD', Data)

# Main Route
@app.route('/')
def indexHTML():
    return render_template('index.html')

global StoreData
StoreData = None
def GETDBCData():
    global StoreData
    while True:
        if StoreData:
            print(StoreData)
            PatientData(StoreData
        time.sleep(4)

ThreadDBC = Thread(target=GETDBCData)
ThreadDBC.start()

#Host webpage onto network
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)

