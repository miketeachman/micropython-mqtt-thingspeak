# The MIT License (MIT)
# Copyright (c) 2018 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Publish data to a Thingspeak channel using the MQTT protocol
#
# Tested using the releases:
#   ESP8266
#       MicroPython 1.9.3
#       MicroPython 1.9.4
#   ESP32
#       MicroPython 1.9.4       (needs addition of MicroPython umqtt module)
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
 
import network
from umqtt.robust import MQTTClient
import time
import os
import gc

#
# WiFi connection information
#   
wifiSSID = "WiFi-SSID"          # EDIT - enter name of WiFi connection point
wifiPassword = "WiFi-PASSWORD"  # EDIT - enter WiFi password 

#
# turn off the WiFi Access Point
# 
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

#
#   connect the ESP8266 device to the WiFi network
#
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(wifiSSID, wifiPassword)

#
# wait until the ESP8266 is connected to the WiFi network
# 
maxAttempts = 20
attemptCount = 0
while not wifi.isconnected() and attemptCount < maxAttempts:
  attemptCount +=1
  time.sleep(1)
  print('did not connect...trying again')
  
#
# create a random MQTT clientID 
#
randomNum = int.from_bytes(os.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

#
# connect to Thingspeak MQTT broker
# connection uses unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses about 9k bytes of the heap
#         (about 1/4 of the micropython heap on the ESP8266 platform)
thingspeakUrl = b"mqtt.thingspeak.com" 
thingspeakUserId = b"USER_ID"          # EDIT - enter Thingspeak User ID
thingspeakMqttApiKey = b"MQTT_API_KEY" # EDIT - enter Thingspeak MQTT API Key
client = MQTTClient(client_id=myMqttClient, 
                    server=thingspeakUrl, 
                    user=thingspeakUserId, 
                    password=thingspeakMqttApiKey, 
                    ssl=False)
                    
client.connect()

#
# publish free heap to Thingspeak using MQTT
#
thingspeakChannelId = b"CHANNEL_ID"             # EDIT - enter Thingspeak Channel ID
thingspeakChannelWriteApiKey = b"WRITE_API_KEY" # EDIT - enter Thingspeak Write API Key
publishPeriodInSec = 30 
while True:
    freeHeapInBytes = gc.mem_free()
    credentials = bytes("channels/{:s}/publish/{:s}".format(thingspeakChannelId, thingspeakChannelWriteApiKey), 'utf-8')  
    payload = bytes("field1={:.1f}\n".format(freeHeapInBytes), 'utf-8')
    client.publish(credentials, payload)
    time.sleep(publishPeriodInSec)
  
client.disconnect()  

