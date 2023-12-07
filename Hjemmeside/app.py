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
import time

#Variables
app = Flask(__name__)
socketio = SocketIO(app)
###Routes
#the main socketio that emites to the webpage
@socketio.on('PatientData')
def socketioPatientData():
    emit('PatientData', {'data': StoreData['PatientData']})

# Main Route
@app.route('/')
def indexHTML():
    return render_template('index.html', data=StoreData)
global StoreData
StoreData = None

def GETDBCData():
    global StoreData
    while True:
        try:
            var1 = DataBaseControl(Conf[0], Conf[1], Conf[2])
            print("var1: ", var1)
            if var1:
                StoreData = var1 
                socketio.emit('PatientData', {'data': StoreData})
                time.sleep(3)
            else:
                print("No data to pass to webpage")
            time.sleep(3)
        except Exception as e:
            print(f"An error cause a faulty pass: {e}")
            pass
ThreadDBC = Thread(target=GETDBCData)
ThreadDBC.daemon = True
ThreadDBC.start()

#Host webpage onto network
if __name__ == '__main__':
    socketio.run(app, host="0.0.0.0", debug=True)

