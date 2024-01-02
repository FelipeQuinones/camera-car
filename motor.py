import RPi.GPIO as GPIO

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