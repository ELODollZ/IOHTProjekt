#!/usr/bin/env python3
# Author: NyboMønster
#IOHT Projekt DHT11

#Liste af imports:
from machine import Pin
import dht

#Liste af Variables
varTemp = 0
varHumi = 0
dhtsensor = dht.DHT11(Pin(25))

def measureFromDHT11():
    varTemp = dhtsensor.temperature()
    varHumi = dhtsensor.humidity()
    #varTemp = 2
    #varHumi = 15
    return varTemp, varHumi
varTemp, varHumi = measureFromDHT11()
print("Temp is:", varTemp, "Humi is:", varHumi)