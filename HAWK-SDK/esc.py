import time  # importing time library to make Rpi wait because its too impatient
from hawk.manager import pwm

ESC = 15  # Connect the ESC in this GPIO pin

PWM = pwm.PWM()
PWM.set_frequency(50)
PWM.set_motor_value(ESC, 0)

max_value = 2000  # change this if your ESC's max value is different or leave it be
min_value = 1000  # change this if your ESC's min value is different or leave it be
print("For first time launch, select calibrate")
print("Type the exact word for the function you want")
print("calibrate OR manual OR control OR arm OR stop")


def manual_drive():  # You will use this function to program your ESC if required
    print("You have selected manual option so give a value between 0 and you max value")
    while True:
        inp = raw_input()
        if inp == "stop":
            stop()
            break
        elif inp == "control":
            control()
            break
        elif inp == "arm":
            arm()
            break
        else:
            PWM.set_motor_value(ESC, int(inp))


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
    print("Controls - a to decrease speed & d to increase speed OR q to decrease a lot of speed & e to increase a lot of speed")
    while True:
        PWM.set_motor_value(ESC, speed)
        inp = raw_input()

        if inp == "q":
            speed -= 100  # decrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "e":
            speed += 100  # incrementing the speed like hell
            print("speed = %d" % speed)
        elif inp == "d":
            speed += 10  # incrementing the speed
            print("speed = %d" % speed)
        elif inp == "a":
            speed -= 10  # decrementing the speed
            print("speed = %d" % speed)
        elif inp == "stop":
            stop()  # going for the stop function
            break
        elif inp == "manual":
            manual_drive()
            break
        elif inp == "arm":
            arm()
            break

    else:
        print("WHAT DID I SAID!! Press a,q,d or e")


def arm():  # This is the arming procedure of an ESC
    print("Connect the battery and press Enter")
    inp = raw_input()
    if inp == '':
        PWM.set_motor_value(ESC, 0)
        time.sleep(1)
        PWM.set_motor_value(ESC, max_value)
        time.sleep(1)
        PWM.set_motor_value(ESC, min_value)
        time.sleep(1)
        control()


def stop():  # This will stop every action your Pi is performing for ESC ofcourse.
    PWM.set_motor_value(ESC, 0)


# This is the start of the program actually, to start the function it needs to be initialized before calling... stupid python.
inp = raw_input()
if inp == "manual":
    manual_drive()
elif inp == "calibrate":
    calibrate()
elif inp == "arm":
    arm()
elif inp == "control":
    control()
elif inp == "stop":
    stop()
else:
    print("Thank You for not following the things I'm saying... now you gotta restart the program STUPID!!")
