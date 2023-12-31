from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import cv2

# Start the Flask app
app = Flask(__name__)

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)

IN1 = 23
IN2 = 24
IN3 = 27
IN4 = 22
SERVO1 = 5
SERVO2 = 6

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(SERVO1, GPIO.OUT)
GPIO.setup(SERVO2, GPIO.OUT)

# Set PWM parameters
pwm_frequency = 50  # Frequency in Hz
duty_cycle1 = 7.5    # Duty cycle (percentage)
duty_cycle2 = 7.5    # Duty cycle (percentage)

# Start PWM
pwm1 = GPIO.PWM(SERVO1, pwm_frequency)
pwm1.start(duty_cycle1)

pwm2 = GPIO.PWM(SERVO2, pwm_frequency)
pwm2.start(duty_cycle2)


# functions to control car movement
def forward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)

def backward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)

def stop():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.LOW)

def left():
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)

def right():
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)

# functions to control camera movement
def cam_up(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle += 1
    if duty_cycle > 12.5:
        duty_cycle = 12.5
    pwm1.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_down(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle -= 1
    if duty_cycle < 2.5:
        duty_cycle = 2.5
    pwm1.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_left(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle += 1
    if duty_cycle > 12.5:
        duty_cycle = 12.5
    pwm2.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_right(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle -= 1
    if duty_cycle < 2.5:
        duty_cycle = 2.5
    pwm2.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

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

@app.route('/camera/<direction>')
def move_camera(direction):
    duty_cycle1 = 7.5    # Duty cycle (percentage)
    duty_cycle2 = 7.5    # Duty cycle (percentage)
    # Control camera movement
    if direction == 'up':
        duty_cycle1 = cam_up(duty_cycle1)
    elif direction == 'down':
        duty_cycle1 = cam_down(duty_cycle1)
    elif direction == 'left':
        duty_cycle2 = cam_left(duty_cycle2)
    elif direction == 'right':
        duty_cycle2 = cam_right(duty_cycle2)
    else:
        return 'Invalid direction', 400
    return 'Camera moved ' + direction, 200

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
        # Stop PWM
        pwm1.stop()
        pwm2.stop()

        # Clean up
        GPIO.cleanup()  # cleanup GPIO settings when the app is terminated