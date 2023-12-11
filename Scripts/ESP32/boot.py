#!/usr/bin/env python3
# Author: NyboMønster

### Imports fra ESP'en selv
import esp
esp.osdebug(None)
#import webrepl
#webrepl.start()
import network
import time
import ubinascii
import micropython
import gc
import random
gc.collect()

### Config Variables
port = 2901
### Credits:
ssid = 'NyboHotSpot'
password = 'Daniel2901Nybo!'
RPI_IP_Add = '192.168.53.56'
ESP32_IP_Add = '192.168.239.88'


### MainCode
station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)


while station.isconnected() == False:
    pass
print('Connection succesful')
print(station.ifconfig())