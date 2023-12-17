import network
import usocket
import time

# Replace with your Wi-Fi credentials
wifi_ssid = "YourWiFiSSID"
wifi_password = "YourWiFiPassword"

# Replace with the local IP address and port of your Raspberry Pi
server_ip = "192.168.29.116"
server_port = 2916

def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    sta_if.active(True)
    sta_if.connect(wifi_ssid, wifi_password)
    while not sta_if.isconnected():
        time.sleep(1)
        print("Connecting to WiFi...")
    print("Connected to WiFi")

def send_test_message():
    addr = usocket.getaddrinfo(server_ip, server_port)[0][-1]

    # Establish a TCP connection
    s = usocket.socket()
    s.connect(addr)
    print("Connected to server")

    # Send a test message
    s.sendall(b"Hello from ESP32!")

    # Close the connection
    s.close()
    print("Connection closed")

# Connect to Wi-Fi
connect_to_wifi()

while True:
    # Send a test message repeatedly
    send_test_message()
    time.sleep(5)
