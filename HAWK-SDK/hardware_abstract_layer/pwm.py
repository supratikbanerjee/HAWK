# Copyright (C) 2017 HAWK-OS

# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at

#    http://www.apache.org/licenses/LICENSE-2.0

# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

# Supratik Banerjee(drakula941)


from hardware_abstract_layer import Adafruit_PCA9685

# import Adafruit_PCA9685
"""PWM class interface between Adafruit_PCA9685 and HawkSDK"""


class PWM:
    def __init__(self):
        """PWM default settings at initialization"""
        self.frequency = 60
        self.pulse_length = 1000000    # 1,000,000 us per second
        self._PWM = Adafruit_PCA9685.PCA9685()
        self._PWM.set_pwm_freq(60)  # set default frequency @60 Hz
        self._PWM.set_all_pwm(0, 0)  # set all pwm values to 0

        # Using 2 dictionaries to map name to channel and channel to name, to save looping.

        self.servoNameList = dict()  # initialize dictionary to map servo name to channel
        self.servoChannelList = dict()  # initialize dictionary to map servo channel to name

        # the same concept of that of servo dictionaries.

        self.motorNameList = dict()  # initialize dictionary to map motor name to channel
        self.motorChannelList = dict()  # initialize dictionary to map motor channel to name

    def set_frequency(self, frequency):
        self.frequency = frequency
        self._PWM.set_pwm_freq(self.frequency)  # set user defined frequency

    def set_pwm_pulsewidth(self, channel, pulse):
        self.pulse_length = 1000000
        self.pulse_length //= self.frequency       # 60 Hz
        # print('{0}us per period'.format(pulse_length))
        self.pulse_length //= 4096     # 12 bits of resolution
        # print('{0}us per bit'.format(pulse_length))
        # pulse *= 1000
        pulse //= self.pulse_length
        self._PWM.set_pwm(channel, 0, pulse)

        '''Servo functions'''

    def set_servo(self, channel, servo_name):
        """map and initialize servo to channel"""
        self.servoNameList[servo_name] = channel  # map user's servo name with channel
        self.servoChannelList[channel] = servo_name  # map servo channel with name

        self._PWM.set_pwm(channel, 0, 0)  # initialize selected channel

    def get_servo_name(self, channel):
        """returns servo name based on servo channel"""
        return self.servoNameList[channel]

    def get_servo_channel(self, servo_name):
        """returns servo chanel based on servo name"""
        return self.servoChannelList[servo_name]

    def set_servo_value(self, channel_name, value):
        """set pwm value for servo"""
        if type(channel_name) is int:  # check for parameter type
            channel = channel_name  # if integer, assign channel as parameter
        else:
            channel = int(self.servoChannelList[channel_name])  # if servo name, map dictionary to retrieve channel
        self.set_pwm_pulsewidth(channel, value)  # assign parameter value to servo

    '''Motor functions'''

    def set_motor(self, channel, motor_name):
        """map and initialize motor to channel"""
        self.motorNameList[motor_name] = channel  # map user's motor name with channel
        self.motorChannelList[channel] = motor_name  # map motor channel with name
        self._PWM.set_pwm(channel, 0, 0)  # initialize selected channel

    def get_motor_name(self, channel):
        """returns servo name based on motor channel"""
        return self.motorNameList[channel]

    def get_motor_channel(self, motor_name):
        """returns servo chanel based on servo name"""
        return self.motorChannelList[motor_name]

    def set_motor_value(self, channel_name, value):
        """set pwm value for motor"""
        if type(channel_name) is int:  # check for parameter type
            channel = channel_name  # if integer, assign channel as parameter
        else:
            channel = int(self.motorChannelList[channel_name])  # if servo name, map dictionary to retrieve channel
        self.set_pwm_pulsewidth(channel, value)  # assign parameter value to servo


class ControlInputToPWM:
    def __init__(self):
        # servo values initialization

        self.servo_mid = 1500
        self.servo_max = 2000
        self.servo_min = 1000
        self.servo_range = 1000

        # motor value initialization

        self.motor_mid = 1500
        self.motor_min = 1000
        self.motor_max = 2000
        self.motor_range = 1000

    def bit_precision_4_mid_map(self, percentage, servo_or_motor):
        x = 0
        y = 0
        percentage -= 5  # since it oscillates between -1 to 1
        percentage *= 2  # multiply to get percentage change
        percentage /= 10.  # divide to get the percentage for 4-bit
        if servo_or_motor == 1:
            x = self.servo_mid  # mid value of servo
            y = (self.servo_range / 2) * float(percentage)  # get the percentage change positive or negative
        elif servo_or_motor == 2:
            x = self.motor_mid  # min value of motor
            y = (self.motor_range / 2) * float(percentage)  # get the percentage change positive or negative
        return int(x + y)  # return mid value + the change in input (+ or -)

    def bit_precision_8_mid_map(self, percentage, servo_or_motor):
        x = 0
        y = 0
        percentage -= 127  # since it oscillates between -1 to 1
        percentage *= 2  # multiply to get percentage change
        percentage /= 255.  # divide to get the percentage for 4-bit
        if servo_or_motor == 1:
            x = self.servo_mid  # mid value of servo
            y = (self.servo_range / 2) * float(percentage)  # get the percentage change positive or negative

        elif servo_or_motor == 2:
            x = self.motor_mid  # mid value of motor
            y = (self.motor_range / 2) * float(percentage)  # get the percentage change positive or negative

        return int(x + y)  # return mid value + the change in input (+ or -)

    def bit_precision_4_full_map(self, percentage, servo_or_motor):
        x = 0
        y = 0
        percentage /= 10.
        if servo_or_motor == 1:
            x = self.servo_min
            y = self.servo_range * float(percentage)
        elif servo_or_motor == 2:
            x = self.motor_min
            y = self.motor_range * float(percentage)

        return int(x + y)

    def bit_precision_8_full_map(self, percentage, servo_or_motor):
        x = 0
        y = 0
        percentage /= 255.
        if servo_or_motor == 1:
            x = self.servo_min
            y = self.servo_range * float(percentage)
        elif servo_or_motor == 2:
            x = self.motor_min
            y = self.motor_range * float(percentage)

        return int(x + y)
