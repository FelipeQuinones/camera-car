from flask import Flask, send_file, render_template
#from picamera import PiCamera
from io import BytesIO
#import RPi.GPIO as GPIO

# Setup GPIO for motor control
#GPIO.setmode(GPIO.BCM)
motor1 = 23  # replace with your GPIO pin
motor2 = 24  # replace with your GPIO pin
#GPIO.setup(motor1, GPIO.OUT)
#GPIO.setup(motor2, GPIO.OUT)

app = Flask(__name__)
#camera = PiCamera()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/capture')
def capture_image():
    # Capture image from camera
    image_stream = BytesIO()
    #camera.capture(image_stream, 'jpeg')
    image_stream.seek(0)
    return send_file(image_stream, mimetype='image/jpeg')

@app.route('/move/<direction>')
def move_car(direction):
    # Control car movement
    if direction == 'forward':
        #GPIO.output(motor1, GPIO.HIGH)
        #GPIO.output(motor2, GPIO.LOW)
        pass
    elif direction == 'backward':
        #GPIO.output(motor1, GPIO.LOW)
        #GPIO.output(motor2, GPIO.HIGH)
        pass
    elif direction == 'stop':
        #GPIO.output(motor1, GPIO.LOW)
        #GPIO.output(motor2, GPIO.LOW)
        pass
    else:
        return 'Invalid direction', 400
    return 'Car moved ' + direction, 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=8000)
    finally:
        pass
        #GPIO.cleanup()  # cleanup GPIO settings when the app is terminated