import Adafruit_DHT
import time
 
class DHT11:
    def __init__(self,):
        DHT_SENSOR = Adafruit_DHT.DHT11

 
    def read_temperatuur(self,DHT_pin):
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            return print("{0:0.1f}".format(temperature))
        # else:
        #     return print("Sensor failure. Check wiring.")
    
    def read_humidity(self,DHT_PIN):
        humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
        if humidity is not None and temperature is not None:
            return print("{0:0.1f}".format(humidity))
        # else:
        #     return print("Sensor failure. Check wiring.")



    