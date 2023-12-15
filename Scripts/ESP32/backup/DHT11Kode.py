#!/usr/bin/env python3
# Author: NyboMønster
# IOHT Projekt DHT11

# List of imports:
from machine import Pin, PWM
import dht
from ConfigFileForESP32 import ListOfConfig as Conf

# List of Variables
varTemp = 0
varHumi = 0
dhtsensor = dht.DHT11(Pin(Conf[0]))

def measureFromDHT11():
    dhtsensor.measure()
    varTemp = dhtsensor.temperature()
    varHumi = dhtsensor.humidity()
    #print("Temp is:", varTemp, "Humi is:", varHumi)
    return varTemp, varHumi

varTemp, varHumi = measureFromDHT11()