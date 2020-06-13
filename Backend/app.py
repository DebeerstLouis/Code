from repositories.DataRepository import DataRepository
from flask import Flask, jsonify, request, url_for, json
from flask_socketio import SocketIO
from flask_cors import CORS
import time
import threading
import Adafruit_DHT
import time
from RPi import GPIO
import time
import socket
from helpers.Lcd import LCD


pins = [16, 12, 25, 24, 23, 26, 19, 13]
clock = 20
rs = 21
def setup_lcd():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(pins, GPIO.OUT)
    GPIO.setup(clock, GPIO.OUT)
    GPIO.setup(rs, GPIO.OUT)
    GPIO.output(clock, 1)

from helpers.Mcp3008 import Mcp3008
Mcp = Mcp3008(0,0)

Motor = 17
Mist = 27
GPIO.setmode(GPIO.BCM)
GPIO.setup(Motor, GPIO.OUT)
GPIO.setup(Mist, GPIO.OUT)

DHT_SENSOR = Adafruit_DHT.DHT11
DHT_PIN = 4
status = 0
app = Flask(__name__)
app.config['SECRET_KEY'] = 'Hier mag je om het even wat schrijven, zolang het maar geheim blijft en een string is'

socketio = SocketIO(app, cors_allowed_origins="*")
CORS(app)

# API ENDPOINTS
@app.route('/')
def hallo():
    return "Server is running, er zijn momenteel geen API endpoints beschikbaar."

@app.route('/temperatuur', methods=["GET"])
def showTemperatuur():
    if request.method == "GET":
        return jsonify(DataRepository.Get_historiek_temperatuur()), 200

@app.route('/Vochtigheid', methods=["GET"])
def showVochtigheid():
    if request.method == "GET":
        return jsonify(DataRepository.Get_historiek_Vochtigheid()), 200

@app.route('/CO', methods=["GET"])
def showCO():
    if request.method == "GET":
        return jsonify(DataRepository.Get_historiek_CO()), 200

@app.route('/Watertank', methods=["GET"])
def showWatertank():
    if request.method == "GET":
        return jsonify(DataRepository.Get_historiek_Watertank()), 200

@app.route('/IP', methods=["GET"])
def getIp():
    if request.method == "GET":
        return jsonify(get_ip_address()), 200


# SOCKET IO
@socketio.on('connect')
def initial_connection():
    print('A new client connected!')

@socketio.on('F2B_alle_aan')
def zetwaarde_aan():
    DataRepository.insert_status_Actuator_by_id(3,1)
    print_naar_lcd_werking_aan()
    print("werking start op")

@socketio.on('F2B_alle_uit')
def zetwaarde_uit():
    DataRepository.insert_status_Actuator_by_id(3,0)
    print_naar_lcd_werking_uit()
    print("werking valt uit")

def lees_Water():
    print("Inlezen van het water niveau")
    x = Mcp.read_channel(0)
    time.sleep(1)
    y = Mcp.read_channel(1)
    waterlevel = (x/1024) * 100
    waarde= round( waterlevel, 2)
    co_Waarde = (y/1024) *100
    co = round(co_Waarde, 2)
    DataRepository.update_status_Sensor_by_id(4, waarde)
    DataRepository.update_status_Sensor_by_id(3, co)
    socketio.emit('B2F_waterniveau', {'waterniveau': waarde})
    socketio.emit('B2F_Co_hoeveelheid', {'Co': co})
    #print(waarde)


def get_ip_address():
 ip_address = ''
 s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
 s.connect(("8.8.8.8",80))
 ip_address = s.getsockname()[0]
 s.close()
 return ip_address




def Werking():
    try:
        while True:
            status = DataRepository.read_status_Actuator_by_id(3)
            statuszelf = status["ActuatorWaarde"]
            if statuszelf == 1:
                humidity, temperature = Adafruit_DHT.read(DHT_SENSOR, DHT_PIN)
                if humidity is not None and temperature is not None:
                    DataRepository.insert_status_Sensor_by_id(1, temperature)
                    DataRepository.insert_status_Sensor_by_id(2, humidity)
                    socketio.emit('B2F_temperatuur', {'temperatuur': temperature})
                    socketio.emit('B2F_humidity', {'humidity': humidity})
                    x = Mcp.read_channel(0)
                    time.sleep(1)
                    y = Mcp.read_channel(1)
                    waterlevel = (x/1024) * 100
                    waarde= round( waterlevel, 2)
                    co_Waarde = (y/1024) *100
                    co = round(co_Waarde, 2)
                    DataRepository.insert_status_Sensor_by_id(4, waarde)
                    DataRepository.insert_status_Sensor_by_id(3, co)
                    socketio.emit('B2F_waterniveau', {'waterniveau': waarde})
                    socketio.emit('B2F_Co_hoeveelheid', {'Co': co})
                    print("alle waarden zijn ingelezen.")
                    
                    vochtigheid = humidity
                    if vochtigheid <= 45 :
                        DataRepository.insert_status_Actuator_by_id(1, 1)
                        time.sleep(40)
                    else:
                        DataRepository.insert_status_Actuator_by_id(1,0)
                        time.sleep(30)
            else:
                DataRepository.insert_status_Actuator_by_id(1,0)
                print("werking uit")
                time.sleep(10)
    finally:
        GPIO.cleanup()
        print("Script has stopped!!!")
                
def Actuatoren():
    while True:
        waardeActu = DataRepository.read_status_Actuator_by_id(1)
        waardezelf = waardeActu["ActuatorWaarde"]
        if waardezelf == 1:
            GPIO.output(Motor, 1)
            GPIO.output(Mist, 1)
            print("motor Aan")
            time.sleep(10)
        else:
            GPIO.output(Mist, 0)
            time.sleep(10)
            GPIO.output(Motor, 0)
            print("motor uit")
            time.sleep(1)


def print_naar_lcd_watertank():
    lcd = LCD(pins, clock, rs)
    lcd.init_lcd()
    lcd.send_string("WAtertank = low", False)

def print_naar_lcd_werking_aan():
    lcd = LCD(pins, clock, rs)
    lcd.init_lcd()
    lcd.send_string("Werking= AAN", False)
    

def print_naar_lcd_werking_uit():
    lcd = LCD(pins, clock, rs)
    lcd.init_lcd()
    lcd.send_string("Werking= UIT", False)
    

def print_naar_lcd():
    lcd = LCD(pins, clock, rs)
    lcd.init_lcd()
    lcd.display_on()
    lcd.reset()
    ip = get_ip_address()
    lcd.send_string("SmartAir", False)
    lcd.send_string("IP=" + ip, True)

print_naar_lcd()

sensoren_lezen = threading.Thread(target=Werking)
Actuatoren_doen = threading.Thread(target=Actuatoren)
time.sleep(2)
sensoren_lezen.start()
Actuatoren_doen.start()

if __name__ == '__main__':
    socketio.run(app,host='0.0.0.0', port=5000 )


