# The MIT License (MIT)
# Copyright (c) 2019 Mike Teachman
# https://opensource.org/licenses/MIT
# 
# Example MicroPython code showing how to use the MQTT protocol to  
# publish data to a Thingspeak channel
#
# User configuration parameters are indicated with "ENTER_".  
 
import network
from umqtt.robust import MQTTClient
import time
import gc
import sys

# Configuration parameters
#=======================================================
WIFI_SSID = 'ENTER_WIFI_SSID'
WIFI_PASSWORD = 'ENTER_WIFI_PASSWORD'
THINGSPEAK_MQTT_CLIENT_ID = b"ENTER_THINGSPEAK_MQTT_CLIENT_ID"
THINGSPEAK_MQTT_USERNAME = b"ENTER_THINGSPEAK_MQTT_USERNAME"
THINGSPEAK_MQTT_PASSWORD = b"ENTER_THINGSPEAK_MQTT_PASSWORD"
THINGSPEAK_CHANNEL_ID = b'ENTER_THINGSPEAK_CHANNEL_ID'
#=======================================================

# turn off the WiFi Access Point
ap_if = network.WLAN(network.AP_IF)
ap_if.active(False)

# connect the device to the WiFi network
wifi = network.WLAN(network.STA_IF)
wifi.active(True)
wifi.connect(WIFI_SSID, WIFI_PASSWORD)

# wait until the device is connected to the WiFi network
MAX_ATTEMPTS = 20
attempt_count = 0
while not wifi.isconnected() and attempt_count < MAX_ATTEMPTS:
    attempt_count += 1
    time.sleep(1)

if attempt_count == MAX_ATTEMPTS:
    print('could not connect to the WiFi network')
    sys.exit()
  
# connect to Thingspeak MQTT broker
# connection uses unsecure TCP (port 1883)
# 
# To use a secure connection (encrypted) with TLS: 
#   set MQTTClient initializer parameter to "ssl=True"
#   Caveat: a secure connection uses more heap space
THINGSPEAK_MQTT_USERNAME = THINGSPEAK_MQTT_CLIENT_ID

client = MQTTClient(server=b"mqtt3.thingspeak.com",
                    client_id=THINGSPEAK_MQTT_CLIENT_ID, 
                    user=THINGSPEAK_MQTT_USERNAME, 
                    password=THINGSPEAK_MQTT_PASSWORD, 
                    ssl=False)
                    
try:            
    client.connect()
except Exception as e:
    print('could not connect to MQTT server {}{}'.format(type(e).__name__, e))
    sys.exit()

# continually publish two fields to a Thingspeak channel using MQTT
PUBLISH_PERIOD_IN_SEC = 20 
while True:
    try:
        freeHeapInBytes = gc.mem_free()
        credentials = bytes("channels/{:s}/publish".format(THINGSPEAK_CHANNEL_ID), 'utf-8')  
        payload = bytes("field1={:.1f}&field2={:.1f}\n".format(freeHeapInBytes, 10.2), 'utf-8')
        client.publish(credentials, payload)
        time.sleep(PUBLISH_PERIOD_IN_SEC)
    except KeyboardInterrupt:
        print('Ctrl-C pressed...exiting')
        client.disconnect()
        wifi.disconnect()
        break