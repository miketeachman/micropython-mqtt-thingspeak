## MQTT protocol with Thingspeak using Micropython on ESP8266
Example code showing how to use the MQTT protocol with the Thingspeak cloud service [https://thingspeak.com]

* Publish data
* Subscribe to data
* Micropython
* ESP8266

## Thingspeak configuration
1. Create a Thingspeak account https://thingspeak.com
1. Create a new Thingspeak channel (select New Channel on the My Channels page)
1. Find the following Thingspeak channel information
    * Channel ID (found at the top of every channel page)
    * User ID (found in Account-> My Profile)
    * Read API Key (found in the API Keys TAB)
    * Write API Key (found in the API Keys TAB)
    * MQTT API Key (found in Account-> My Profile)

## Example code configuration
* The code is commented at various places with **"EDIT"** indicating places where Thingspeak configuration
parameters are needed 

## Limitations
* no exception handling in example code
* examples support only one field in the channel

## Hardware
* tested with Adafruit Feather HUZZAH ESP8266
* two ESP8266s used.  One to Publish data.  2nd to Subscribe.

## Micropython Version
* tested with Micropython v1.9.3 (November 1, 2017)

## Recommended Tools
* Adafruit Ampy
    * install version 1.0.3 which has the -d option (use **-d1** to avoid USB connection issues in Windows)
* Putty

## Making it work
1. Configure example code with Thingspeak parameters
1. Use Ampy to put Publish code to main.py on ESP8266
1. Reset ESP8266
1. Observe that data is being Published to the Thingspeak channel at Thingspeak.com
1. Use Ampy to put Subscribe code to main.py on 2nd ESP8266
1. Reset the 2nd ESP8266
1. Connect to 2nd ESP8266 with Putty
1. Observe in Putty window that Subscribed data is being received by ESP8266






