## MQTT protocol with Thingspeak using Micropython
Example code showing how to use the MQTT protocol with the Thingspeak cloud service [https://thingspeak.com]

* Publish data
* Subscribe to data

## Thingspeak configuration
1. Create a Thingspeak account https://thingspeak.com
1. Create a new Thingspeak Channel (select New Channel on the My Channels page)
    * the `Channel ID` is required for configuration (found at the top of every channel page)
1. Create a new MQTT Device by following instructions in https://www.mathworks.com/help/thingspeak/mqtt-basics.html
    * when you create a new MQTT device it is important to record the three configuration parameters:
        * `MQTT Client ID` 
        * `MQTT Username` 
        * `MQTT Password` (careful - you can only copy the password during the MQTT device creation step)
  
## Example code configuration
* The code includes variables with the form **"ENTER_"** indicating places where WiFi and Thingspeak configuration
parameters are needed 

## Tested with Hardware
* Adafruit Feather HUZZAH ESP8266
* Adafruit Feather HUZZAH ESP32
* WeMos D1 Mini
* Lolin D32
* Lolin D32 Pro
* Pyboard D  (note: requires UMQTT library to be installed)

## Tested with Micropython Versions
* Micropython v1.19.1

### Recommended Tools for Windows
* Adafruit Ampy to copy files to the filesystem
    * install version 1.0.3 or newer which has the -d option (use **-d1** to avoid USB connection issues in Windows)
* Putty to interact with the REPL  
    * set Serial speed to 115200 and Flow control to None

## Publishing data to ThingSpeak channels

#### Usage
1. Configure code file _publishThingspeak.py_ with WiFi and ThingSpeak configuration parameters
1. Copy the file _publishThingspeak.py_ to your device, using [ampy](https://github.com/scientifichackers/ampy), [rshell](https://github.com/dhylands/rshell), or [webrepl](http://micropython.org/webrepl/)
```
$ ampy -pCOMx -d1 put publishThingspeak.py main.py
```
1. Reset the board
1. Observe that data is being Published to the ThingSpeak channel at Thingspeak.com

## Subscribing to ThingSpeak channels (still to be updated)

#### Usage
1. Configure code file _subscribeThingspeak.py_ with ThingSpeak parameters
1. Copy the file _subscribeThingspeak.py_ to your device, using [ampy](https://github.com/scientifichackers/ampy), [rshell](https://github.com/dhylands/rshell), [webrepl](http://micropython.org/webrepl/)
```
$ ampy -pCOMx -d1 put subscribeThingspeak.py main.py
```
4. Configure a 2nd device to publish the freeHeap data (see above)
1. Reset the board
1. Connect to the REPL with Putty (or simlar) to observe subscribed channel data being received (every 30s in the example code)

## Installing UMQTT Package for Pyboard D
The example code requires the MicroPython MQTT (UMQTT) Package.  Pyboard D firmware does not have this package built-in

##### How to install the UMQTT package
1. Navigate to [Micropython lib](https://github.com/micropython/micropython-lib 
1. Select the "Clone or download" button
1. Select "Download ZIP"
1. Extract the ZIP.  Should see folder called "micropython-lib-master"
1. Two files need to be copied to the MicroPython filesystem
    * micropython-lib\micropython\umqtt.simple\umqtt\simple.py
    * micropython-lib\micropython\umqtt.robust\umqtt\robust.py
  
Copy these two files to the MicroPython filesystem with the directory structure shown below.  

```
boot.py
lib
  |
  umqtt
     simple.py
     robust.py
```

Example with Ampy:    
```
>ampy -pCOM27 -d1 ls
boot.py
>ampy -pCOM27 -d1 mkdir lib
>ampy -pCOM27 -d1 mkdir lib/umqtt
>ampy -pCOM27 -d1 put simple.py lib/umqtt/simple.py
>ampy -pCOM27 -d1 put robust.py lib/umqtt/robust.py
>ampy -pCOM27 -d1 ls
boot.py
lib
>ampy -pCOM27 -d1 ls lib
umqtt
>ampy -pCOM27 -d1 ls lib/umqtt
simple.py
robust.py
```
##### Validating the UMQTT package install
From the REPL (using Putty, etc) execute the following commands and observe similar output
```
>>> from umqtt.robust import MQTTClient

>>> dir(MQTTClient)
['__class__', '__init__', '__module__', '__name__', '__qualname__', '__bases__', '__dict__', 'connect', 'delay', 'disconnect', 'log', 'DEBUG', 'DELAY', 'reconnect', 'publish', 'wait_msg', '_send_str', '_recv_len', 'set_callback', 'set_last_will', 'ping', 'subscribe', 'check_msg']
```

If you see this result you have successfully installed the umqtt package. :tada: :relieved: