
import RPi.GPIO as GPIO
from datetime import datetime
import time
import threading

GPIO.setwarnings(False)

# Pin Definitions
input_pin = 21  # BCM pin 21

# Globals to control the thread and read the counter
running = False
ttl_counter = 0
ttl_time = datetime.now()


def gpio_counter(channel):
    global ttl_counter
    global ttl_time
    ttl_counter +=1
    ttl_time = datetime.now()


def accurate_delay(delay):
    """
    Function to provide accurate time delay in millisecond
    :param delay: Delay in milliseconds
    :return: Nothing
    """
    target_time = time.perf_counter() + delay/1000
    while time.perf_counter() < target_time:
        pass


def start_ttl_counter():
    global ttl_counter
    global current_time

    # Pin Setup:
    GPIO.setmode(GPIO.BCM)  # BCM pin-numbering scheme from Raspberry Pi
    GPIO.setup(input_pin, GPIO.IN)  # set pin as an input pin

    while not running:
        accurate_delay(1)

    try:
        while running:
            GPIO.wait_for_edge(input_pin, GPIO.RISING)
            gpio_counter(input_pin)

    finally:
        GPIO.cleanup()

thread = threading.Thread(group=None, target=start_ttl_counter, daemon=True)
thread.start()