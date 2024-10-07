from flask import Flask
import RPi.GPIO as GPIO
import time
import subprocess

app = Flask(__name__)

GPIO.setmode(GPIO.BOARD)

pin_fan = 13

GPIO.setup(pin_fan, GPIO.OUT)
current_state = "isOn"

mp3_roundstart = "/home/pi/Desktop/cs2glassreceiver/roundstart.mp3"
mp3_roundend = "/home/pi/Desktop/cs2glassreceiver/roundend.mp3"

commandstart = ["vlc", mp3_roundstart, "--intf", "dummy", "--play-and-exit"]
commandend = ["vlc", mp3_roundend, "--intf", "dummy", "--play-and-exit"]



@app.route('/turn_on')
def turn_on():
    global current_state
    if current_state == "isOff": 
        GPIO.output(pin_fan, GPIO.HIGH)
        time.sleep(0.2)
        GPIO.output(pin_fan, GPIO.LOW)
        current_state = "isOn"
        subprocess.run(commandstart)

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
        subprocess.run(commandend)

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
