from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import cv2

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

# functions to control car movement
def forward():
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in2, GPIO.LOW)
    print("forward")

def backward():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.HIGH)
    print("backward")

def stop():
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)
    print("stop")

def left():
    GPIO.output(in3, GPIO.HIGH)
    GPIO.output(in4, GPIO.LOW)
    print("left")

def right():
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.HIGH)
    print("right")

# function to capture image
def gen(camera):
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

############################################################################################################
# route for serving video stream
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()), mimetype='multipart/x-mixed-replace; boundary=frame')

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

############################################################################################################
# class to capture image
class Camera(object):
    def __init__(self):
        self.video = cv2.VideoCapture(0)  # Use 0 for the default camera

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        if success:
            # If reading the frame was successful, encode the image
            _, jpeg = cv2.imencode('.jpg', image)
            return jpeg.tobytes()
        else:
            # If reading the frame was not successful, return a default image
            with open('default.jpg', 'rb') as f:
                return f.read()

if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=80)
    finally:
        GPIO.cleanup()  # cleanup GPIO settings when the app is terminated