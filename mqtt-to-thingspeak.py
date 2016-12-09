# The MIT License (MIT)
# Copyright (c) 2016 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Publish data to Thingspeak channels using the MQTT protocol
#
# Micropython implementation using the ESP8266 platform
# Micropython version:  esp8266-20161110-v1.8.6.bin
#
# Hardware used:
# - Adafruit Huzzah ESP8266 running micropython  
# - Adafruit MCP9808 temperature breakout board
# - USB to serial converter
#
# prerequisites:
# - Thingspeak account
# - Thingspeak channel to receive data
#
# References:
#
# These 3 videos by Tony DiCola/Adafruit.  See adafruit.com website
#   1. MicroPython Basics: How to Load MicroPython on a Board
#	2. MicroPython Basics: Load Files & Run Code 
#   3. MicroPython Hardware: I2C Devices 
#     
 
import machine
import network
import time
import gc
from umqtt.simple import MQTTClient

#
# conversion routine, MCP9808 2-byte response --> Degrees C (courtesy of Tony DiCola)
#
def convertMCP9808ToDegC(data):
    value = data[0] << 8 | data[1]
    temp = (value & 0xFFF) / 16.0
    if value & 0x1000:
        temp -= 256.0
    return temp

#
# configure I2C for communication to MCP9808 sensor hardware
#
i2c = machine.I2C(machine.Pin(5), machine.Pin(4))

#
# connect the ESP8266 to local wifi network
#
yourWifiSSID = "YOUR-NETWORK-SSID" # <--- replace with your WIFI network name
yourWifiPassword = "YOUR-NETWORK-PWD" # <--- replace with your WIFI network password
sta_if = network.WLAN(network.STA_IF)
sta_if.active(True)
sta_if.connect(yourWifiSSID, yourWifiPassword)
while not sta_if.isconnected():
  pass
  
#
# connect ESP8266 to Thingspeak using MQTT
#
myMqttClient = "my-mqtt-client"  # can be anything unique
thingspeakIoUrl = "mqtt.thingspeak.com" 
c = MQTTClient(myMqttClient, thingspeakIoUrl, 1883)  # uses unsecure TCP connection
c.connect()

#
# publish temperature and free heap to Thingspeak using MQTT
#
i2cDeviceAddress = 24
i2cRegisterAddress = 5
i2cNumBytesToRead = 2
thingspeakChannelId = "YOUR-CHANNEL-ID"  # <--- replace with your Thingspeak Channel ID
thingspeakChannelWriteapi = "YOUR-CHANNEL-WRITEAPIKEY" # <--- replace with your Thingspeak Write API Key
publishPeriodInSec = 30 
while True:
  dataFromMCP9808 = i2c.readfrom_mem(i2cDeviceAddress, i2cRegisterAddress, i2cNumBytesToRead)  # read temperature from sensor using i2c
  tempInDegC = convertMCP9808ToDegC(dataFromMCP9808)
  
  # note:  string concatenations below follow best practices as described in micropython reference doc
  credentials = "channels/{:s}/publish/{:s}".format(thingspeakChannelId, thingspeakChannelWriteapi)  
  payload = "field1={:.1f}&field2={:d}\n".format(tempInDegC, gc.mem_free())
  c.publish(credentials, payload)
  
  time.sleep(publishPeriodInSec)
  
c.disconnect()  

