from flask import Flask, render_template, Response
import RPi.GPIO as GPIO
import cv2
import motor

# Start the Flask app
app = Flask(__name__)

GPIO.setwarnings(False)  # Disable GPIO warnings
GPIO.setmode(GPIO.BCM)

IN1 = 23 #(02, M)
IN2 = 24 #(02, L)
IN3 = 27
IN4 = 22
SERVO1 = 6 # servo izquierda/derecha
SERVO2 = 5 # servo arriba/abajo

GPIO.setup(IN1, GPIO.OUT)
GPIO.setup(IN2, GPIO.OUT)
GPIO.setup(IN3, GPIO.OUT)
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(SERVO1, GPIO.OUT)
GPIO.setup(SERVO2, GPIO.OUT)

# Set PWM parameters
pwm_frequency = 50  # Frequency in Hz
duty_cycle1 = 7.5   # Duty cycle (percentage)
duty_cycle2 = 7.5   # Duty cycle (percentage)

stop_flag = False

# Start PWM
pwm1 = GPIO.PWM(SERVO1, pwm_frequency)
pwm1.start(duty_cycle1)

pwm2 = GPIO.PWM(SERVO2, pwm_frequency)
pwm2.start(duty_cycle2)

STEPS = 0.001  # Duty cycle increase/decrease amount for each servo movement

# functions to control camera movement
def cam_down(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle += STEPS
    if duty_cycle > 11:
        duty_cycle = 11
    print(duty_cycle)
    pwm1.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_up(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle -= STEPS
    if duty_cycle < 4:
        duty_cycle = 4
    print(duty_cycle)
    pwm1.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_left(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle += STEPS
    if duty_cycle > 11:
        duty_cycle = 11
    pwm2.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_right(duty_cycle):
    # Change the duty cycle to move the servo
    duty_cycle -= STEPS
    if duty_cycle < 4:
        duty_cycle = 4
    pwm2.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_stop():
    # Stop the PWM
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

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
        motor.forward(IN1, IN2, IN3, IN4)
    elif direction == 'backward':
        motor.backward(IN1, IN2, IN3, IN4)
    elif direction == 'left':
        motor.left(IN1, IN2, IN3, IN4)
    elif direction == 'right':
        motor.right(IN1, IN2, IN3, IN4)
    elif direction == 'forward_left':
        motor.forward_left(IN1, IN2, IN3, IN4)
    elif direction == 'forward_right':
        motor.forward_right(IN1, IN2, IN3, IN4)
    elif direction == 'backward_left':
        motor.backward_left(IN1, IN2, IN3, IN4)
    elif direction == 'backward_right':
        motor.backward_right(IN1, IN2, IN3, IN4)
    elif direction == 'stop':
        motor.stop(IN1, IN2, IN3, IN4)
    else:
        return 'Invalid direction', 400
    return 'Car moved ' + direction, 200

@app.route('/camera/<direction>')
def move_camera(direction):
    global duty_cycle1, duty_cycle2, stop_flag
    stop_flag = False

    # Control camera movement
    if direction == 'up':
        while not stop_flag:
            duty_cycle1 = cam_up(duty_cycle1)
    elif direction == 'down':
        while not stop_flag:
            duty_cycle1 = cam_down(duty_cycle1)
    elif direction == 'left':
        while not stop_flag:
            duty_cycle2 = cam_left(duty_cycle2)
    elif direction == 'right':
        while not stop_flag:
            duty_cycle2 = cam_right(duty_cycle2)
    else:
        return 'Invalid direction', 400
    cam_stop()
    return 'Camera moved ' + direction, 200

@app.route('/camera/stop')
def stop_camera():
    global stop_flag
    cam_stop()
    stop_flag = True
    return "Stopping camera"

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
            with open('images/default.jpg', 'rb') as f:
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