import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin where the servo is connected
SERVO_PIN = 5

# Set the GPIO pin as output
GPIO.setup(SERVO_PIN, GPIO.OUT)

# Set PWM parameters
pwm_frequency = 50  # Frequency in Hz
duty_cycle = 7.5    # Duty cycle (percentage)

# Start PWM
pwm = GPIO.PWM(SERVO_PIN, pwm_frequency)
pwm.start(duty_cycle)

try:
    while True:
        # Change the duty cycle to move the servo
        pwm.ChangeDutyCycle(7.5)  # 0 degrees
        time.sleep(1)
        pwm.ChangeDutyCycle(12.5)  # 90 degrees
        time.sleep(1)
        pwm.ChangeDutyCycle(2.5)  # 180 degrees
        time.sleep(1)
finally:
    # Stop PWM
    pwm.stop()

    # Clean up
    GPIO.cleanup()