import picamera
from picamera import PiCamera
from picamera.exc import PiCameraError, PiCameraMMALError
from flask import Flask, render_template, send_file
from io import BytesIO
import RPi.GPIO as GPIO

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)

in1 = 23
in2 = 24
in3 = 27
in4 = 22


GPIO.setup(in1, GPIO.OUT)
GPIO.setup(in2, GPIO.OUT)
GPIO.setup(in3, GPIO.OUT)
GPIO.setup(in4, GPIO.OUT)

app = Flask(__name__)

try:
    camera = PiCamera()
except PiCameraError:
    print("Camera is not enabled or not available.")
    camera = None

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
    image_stream = BytesIO()
    if camera is not None:
        try:
            # Try to capture an image from the camera
            camera.capture(image_stream, 'jpeg')
        except picamera.exc.PiCameraMMALError:
            # If capturing the image fails, return a default image
            with open('default.png', 'rb') as f:
                image_stream.write(f.read())
    else:
        # If the camera is not available, return a default image
        with open('default.png', 'rb') as f:
            image_stream.write(f.read())
    image_stream.seek(0)
    return send_file(image_stream, mimetype='image/jpeg')

@app.route('/move/<direction>')
def move_car(direction):
    # Control car movement
    if direction == 'forward':
        forward()
    elif direction == 'backward':
        backward()
    elif direction == 'left':
        left()
    elif direction == 'right':
        right()
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