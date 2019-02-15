# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Example MicroPython code showing how to use the MQTT protocol to  
# publish data to a Thingspeak channel
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
# - Thingspeak channel to publish data
# - Thingspeak Write API Key for the channel
# - Thingspeak MQTT API Key for the account
#
# User configuration parameters are indicated with "ENTER_".  
 
import network
from umqtt.robust import MQTTClient
import time
import os
import gc
import sys

# WiFi connection information
wifiSSID = '<ENTER_WIFI_SSID>'
wifiPassword = '<ENTER_WIFI_PASSWORD>'

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
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
  
# create a random MQTT clientID 
randomNum = int.from_bytes(os.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

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
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# publish free heap statistics to Thingspeak using MQTT
THINGSPEAK_CHANNEL_ID = b'<ENTER_CHANNEL_ID>'
THINGSPEAK_CHANNEL_WRITE_API_KEY = b'<ENTER_CHANNEL_WRITE_API_KEY>'
PUBLISH_PERIOD_IN_SEC = 30 
while True:
    try:
        freeHeapInBytes = gc.mem_free()
        credentials = bytes("channels/{:s}/publish/{:s}".format(THINGSPEAK_CHANNEL_ID, THINGSPEAK_CHANNEL_WRITE_API_KEY), 'utf-8')  
        payload = bytes("field1={:.1f}\n".format(freeHeapInBytes), 'utf-8')
        client.publish(credentials, payload)
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        sys.exit()    