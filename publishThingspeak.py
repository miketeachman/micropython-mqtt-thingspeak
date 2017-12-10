# The MIT License (MIT)
# Copyright (c) 2017 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Publish data to a Thingspeak channel using the MQTT protocol
#
# Micropython implementation using the ESP8266 platform
# Tested using Micropython v1.9.3 (Nov 1, 2017)
#
# Tested using Hardware:
# - Adafruit Feather HUZZAH ESP8266 
#
# prerequisites:
# - Thingspeak account
# - Thingspeak channel to publish data
# - Thinkspeak Write API Key for the channel
# - Thinkspeak MQTT API Key for the account
#
 
import network
from umqtt.robust import MQTTClient
import utime
import uos
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
  utime.sleep(1)
  print('did not connect...trying again')
  
#
# create a random MQTT clientID 
#
randomNum = int.from_bytes(uos.urandom(3), 'little')
myMqttClient = bytes("client_"+str(randomNum), 'utf-8')

#
# connect to Thingspeak MQTT broker
# connection uses unsecure TCP (port 1883)
# 
# Steps to change to a secure connection (encrypted) using TLS
#   a) change port below to "port=8883
#   b) add parameter "ssl=True"
#   NOTE:  TLS uses about 9k bytes of the heap. That is a lot.
#          (about 1/4 of the micropython heap on the ESP8266 platform)
#
thingspeakUrl = b"mqtt.thingspeak.com" 
thingspeakUserId = b"USER_ID"          # EDIT - enter Thingspeak User ID
thingspeakMqttApiKey = b"MQTT_API_KEY" # EDIT - enter Thingspeak MQTT API Key
client = MQTTClient(client_id=myMqttClient, 
                    server=thingspeakUrl, 
                    user=thingspeakUserId, 
                    password=thingspeakMqttApiKey, 
                    port=1883)
                    
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
    utime.sleep(publishPeriodInSec)
  
client.disconnect()  

