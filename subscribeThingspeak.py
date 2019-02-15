# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Subscribe to data from a Thingspeak channel using the MQTT protocol
#
# Tested using the releases:
#   ESP8266
#       MicroPython 1.9.3
#       MicroPython 1.9.4
#       MicroPython 1.10
#   ESP32
#       MicroPython 1.9.4       (needs addition of MicroPython umqtt module)
#       MicroPython 1.10
#
# Tested using the following boards:
#   Adafruit Feather HUZZAH ESP8266
#   Adafruit Feather HUZZAH ESP32
#   WeMos D1 Mini
#
# prerequisites:
# - Thingspeak account
# - Thingspeak channel with published data
# - Thingspeak Read API Key for the channel
# - Thingspeak MQTT API Key for the account
#
# User configuration parameters are indicated with "ENTER_".  
# User configuration parameters are indicated with "ENTER_".  

import network
from umqtt.robust import MQTTClient
import time
import os
import sys

def cb(topic, msg):
    print((topic, msg))
    freeHeap = float(str(msg,'utf-8'))
    print("free heap size = {} bytes".format(freeHeap))

# WiFi connection information
wifiSSID = '<ENTER_WIFI_SSID>'
wifiPassword = '<ENTER_WIFI_PASSWORD>'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the ESP8266 device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifiSSID, wifiPassword)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()
  
# create a random clientID 
randomNum = int.from_bytes(os.urandom(3), 'little')
myMqttClient = bytes("client"+str(randomNum), 'utf-8')

# connect to Thingspeak MQTT broker
# connection uses unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
THINGSPEAK_URL = b"mqtt.thingspeak.com" 
THINGSPEAK_USER_ID = b'<ENTER_USER_ID>'
THINGSPEAK_MQTT_API_KEY = b'<ENTER_MQTT_API_KEY>'
client = MQTTClient(client_id=myMqttClient, 
                    server=THINGSPEAK_URL, 
                    user=THINGSPEAK_USER_ID, 
                    password=THINGSPEAK_MQTT_API_KEY, 
                    ssl=False)

# callback to handle data when MQTT channel updates  
client.set_callback(cb)
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# subscribe a Thingspeak channel field using MQTT
THINGSPEAK_CHANNEL_ID = b'<ENTER_CHANNEL_ID>'
THINGSPEAK_CHANNEL_READ_API_KEY = b'<ENTER_CHANNEL_READ_API_KEY>'
subscribeTopic = bytes("channels/{:s}/subscribe/fields/field1/{:s}".format(THINGSPEAK_CHANNEL_ID, THINGSPEAK_CHANNEL_READ_API_KEY), 'utf-8')  
client.subscribe(subscribeTopic)

# wait until data has been Published to the Thingspeak channel
while True:
    try:
        client.wait_msg()
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()

