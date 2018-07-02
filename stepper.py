import sys
import RPi.GPIO as gpio  # https://pypi.python.org/pypi/RPi.GPIO more info
import time

print("Vroem")
direction1 = sys.argv[1]
direction2 = sys.argv[3]
steps1 = int(float(sys.argv[2]))
steps2 = int(float(sys.argv[4]))

# print("You told me to turn %s %s steps.") % (globals(direction), steps)

gpio.setmode(gpio.BCM)
# GPIO23 = Direction
# GPIO24 = Step
gpio.setup(17, gpio.OUT)
gpio.setup(23, gpio.OUT)
gpio.setup(24, gpio.OUT)
gpio.setup(27, gpio.OUT)

if direction1 == 'left':
    gpio.output(27, True)
elif direction1 == 'right':
    gpio.output(27, False)

if direction2 == 'left':
    gpio.output(24, True)
elif direction2 == 'right':
    gpio.output(24, False)

if steps1 > steps2:
    MaxSteps = steps1
else:
    MaxSteps = steps2

StepCounter1 = 0
StepCounter2 = 0
TotalCounter = 0

StepTime = 1
WaitTime = 0.0001

# Start main loop
while StepCounter1 < MaxSteps:
    # turning the gpio on and off tells the easy driver to take one step
    if StepCounter1 < steps1:
        # time.sleep(0.5 / steps1)
        gpio.output(17, True)
        gpio.output(17, False)
        StepCounter1 += 1
    #
    if StepCounter2 < steps2:
        # time.sleep(0.5 / steps2)
        gpio.output(23, True)
        gpio.output(23, False)
        StepCounter2 += 1

    TotalCounter += 1
    # Wait before taking the next step...this controls rotation speed
    time.sleep(WaitTime)

gpio.cleanup()
