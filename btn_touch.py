import RPi.GPIO as GPIO
import time

# Pin connected to the capacitive touch switch
BTN1 = 18 # purple orange blue
BTN2 = 23 # yellow green blue

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setup(BTN1, GPIO.IN)
    GPIO.setup(BTN2, GPIO.IN)

def loop():
    while True:
        if GPIO.input(BTN1):
            print("btn1")
        
        if GPIO.input(BTN2):
            print("btn2")
        
        time.sleep(0.1)

def destroy():
    GPIO.cleanup()

if __name__ == '__main__':
    print('Press Ctrl+C to end the program.')
    setup()
    try:
        loop()
    except KeyboardInterrupt:
        destroy()