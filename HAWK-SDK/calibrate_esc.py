import time
from hawk.manager import pwm

ESC = 15  # Connect the ESC in this GPIO pin

PWM = pwm.PWM()
PWM.set_motor_value(ESC, 0)
max_value = 2000
min_value = 1000

def calibrate():  # This is the auto calibration procedure of a normal ESC
    PWM.set_motor_value(ESC, 0)
    print("Disconnect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        PWM.set_motor_value(ESC, max_value)
        print("Connect the battery NOW.. you will here two beeps, then wait for a gradual falling tone then press Enter")
        inp = raw_input()
        if inp == '':
            PWM.set_motor_value(ESC, min_value)
            print("Wierd eh! Special tone")
            time.sleep(5)
            print("Wait for it ....")
            time.sleep(5)
            print("Im working on it, DONT WORRY JUST WAIT.....")
            PWM.set_motor_value(ESC, 0)
            time.sleep(2)
            print("Arming ESC now...")
            PWM.set_motor_value(ESC, min_value)
            time.sleep(1)
            print("See.... uhhhhh")
            control()  # You can change this to any other function you want


def control():
    print("I'm Starting the motor, I hope its calibrated and armed, if not restart by giving 'x'")
    time.sleep(1)
    speed = 1500  # change your speed if you want to.... it should be between 700 - 2000