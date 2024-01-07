import RPi.GPIO as GPIO

STEPS = 0.00005  # Duty cycle increase/decrease amount for each servo movement

def stop(in1, in2, in3, in4):
    GPIO.output(in1, GPIO.LOW)
    GPIO.output(in2, GPIO.LOW)
    GPIO.output(in3, GPIO.LOW)
    GPIO.output(in4, GPIO.LOW)

def forward(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in1, GPIO.HIGH)

def backward(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in2, GPIO.HIGH)

def left(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in3, GPIO.HIGH)

def right(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in4, GPIO.HIGH)

def forward_left(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)

def forward_right(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in1, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

def backward_left(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in3, GPIO.HIGH)

def backward_right(in1, in2, in3, in4):
    stop(in1, in2, in3, in4)
    GPIO.output(in2, GPIO.HIGH)
    GPIO.output(in4, GPIO.HIGH)

# functions to control camera movement
def cam_down(duty_cycle, pwm):
    # Change the duty cycle to move the servo
    duty_cycle += STEPS
    if duty_cycle > 11:
        duty_cycle = 11
    pwm.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_up(duty_cycle, pwm):
    # Change the duty cycle to move the servo
    duty_cycle -= STEPS
    if duty_cycle < 4:
        duty_cycle = 4
    pwm.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_left(duty_cycle, pwm):
    # Change the duty cycle to move the servo
    duty_cycle += STEPS
    if duty_cycle > 11:
        duty_cycle = 11
    pwm.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_right(duty_cycle, pwm):
    # Change the duty cycle to move the servo
    duty_cycle -= STEPS
    if duty_cycle < 4:
        duty_cycle = 4
    pwm.ChangeDutyCycle(duty_cycle)  # 0 degrees
    return duty_cycle

def cam_stop(pwm1, pwm2):
    # Stop the PWM
    pwm1.ChangeDutyCycle(0)
    pwm2.ChangeDutyCycle(0)

def cam_center(pwm1, pwm2):
    # Change the duty cycle to move the servo
    pwm1.ChangeDutyCycle(7.5)  # 0 degrees
    pwm2.ChangeDutyCycle(7.5)  # 0 degrees