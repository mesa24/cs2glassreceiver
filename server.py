from flask import Flask
import RPi.GPIO as GPIO
import time
import playsound

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)

pin_fan = 13

GPIO.setup(pin_fan, GPIO.OUT)
current_state = "isOn"

@app.route('/turn_on')
def turn_on():
    global current_state
    if current_state == "isOff": 
        GPIO.output(pin_fan, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin_fan, GPIO.LOW)
        current_state = "isOn"
        playsound.playsound('/home/pi/Desktop/cs2glassreceiver/sfx.mp3', True)

        return 'Fan turned on'
    else:
        return 'Fan is already on'

@app.route('/turn_off')
def turn_off():
    global current_state
    if current_state == "isOn":
        GPIO.output(pin_fan, GPIO.HIGH) 
        time.sleep(0.2)
        GPIO.output(pin_fan, GPIO.LOW)
        current_state = "isOff"
        return 'Fan turned off'
    else:
        return 'Fan is already off'

@app.route('/switch')
def switch():
    GPIO.output(pin_fan, GPIO.HIGH)
    time.sleep(0.2)
    GPIO.output(pin_fan, GPIO.LOW)
    return 'Glass switched successfully.'

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    finally:
        GPIO.cleanup()
