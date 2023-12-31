#!/usr/bin/env python3
# Author: NyboMønster

#Imports
import sys
sys.path.insert(0, '/home/Gruppe2PI/Projekts/IOHTProjekt/Scripts')
from flask import Flask, render_template, request, jsonify
from flask_socketio import SocketIO, emit
from ConfigFile import ListOfConfig as Conf
from PatientIndexing import DataBaseControl
from threading import Thread
import time
import logging

#Variables
app = Flask(__name__)
socketio = SocketIO(app)
global DataArray, varTemp, varHumi, varServo
DataArray = None
varTemp = None
varHumi = None
varServo = None
###Routes
#the main socketio that emites to the webpage
@socketio.on('PatientData')
def socketioPatientData():
    global StoreData
    emit('PatientData', {'data': StoreData})

@app.route('/ESP32Data', methods=['POST'])
def GetDataFromESP32():
    try:
        data = request.get_json(force=True)
        print(data)
        varTemp = data.get("Temp", "").replace("Temp: ", "")
        varHumi = data.get("Humidity", "").replace("Humidity: ", "")
        varServo = data.get("ServoOutput", "").replace("ServoOutput: ", "")
        print(varTemp, varHumi, varServo)
        return jsonify({
            "Success": True, 
            "Message": "Data recieved successfully:",
            "Temp": varTemp,
            "Humidity": varHumi,
            "ServoOutput": varServo
            })
    except Exception as e:
        return jsonify({"Success": False, "error": str(e)})

# Main Route
@app.route('/')
def indexHTML():
    return render_template('index.html', data=StoreData, Temp=varTemp, Humi=varHumi, ServoOutPut=varServo)
global StoreData
StoreData = None

def GETDBCData():
    prevVar1 = None
    while True:
        try:
            var1 = DataBaseControl(Conf[0], Conf[1], Conf[2])
            if var1 is not None:
                global StoreData
                if var1 != prevVar1:
                    StoreData = var1
                    socketio.emit('PatientData', {'data': StoreData})
                    prevVar1 = var1
            else:
                StoreData = None
                print("No data to pass to webpage")
                time.sleep(1)
                pass
            time.sleep(3)
        except Exception as e:
            print(f"An error cause a faulty pass: {e}")
ThreadDBC = Thread(target=GETDBCData)
ThreadDBC.daemon = True
ThreadDBC.start()

#Logging the outputs
handler = logging.FileHandler('FlaskApp.log')
handler.setLevel(logging.INFO)
app.logger.addHandler(handler)
#Host webpage onto network
if __name__ == '__main__':
    socketio.run(app, host=Conf["RPIServerAddress"], port=Conf["RPIPortNumber"], debug=True)

