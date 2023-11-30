#!/usr/bin/env python3
# Author: NyboMønster
#IOHT Projekt DHT11

#Liste af imports:
from machine import Pin
import dht

#Liste af Variables
varTemp = 0
varHumi = 0


def measureFromDHT11():
    varTemp = dht.temperature
    varHumi = dht.humidity
    #varTemp = 2
    #varHumi = 15
    print("Temp is:", varTemp, "Humi is:", varHumi)
    return varTemp, varHumi
    
#measureFromDHT11()