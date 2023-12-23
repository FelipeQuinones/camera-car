import RPi.GPIO as GPIO
from flask import Flask, send_file, render_template
#from picamera import PiCamera
from io import BytesIO

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)

in1 = 23
in2 = 24
in3 = 27
in4 = 22


GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)

app = Flask(__name__)
#camera = PiCamera()

def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)

def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)

def left():
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)

def right():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)

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
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'stop':
        stop()
    else:
        return 'Invalid direction', 400
    return 'Car moved ' + direction, 200

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        GPIO.cleanup()  # cleanup GPIO settings when the app is terminated