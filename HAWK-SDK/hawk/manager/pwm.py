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


from hardware_abstract_layer.pwm import PWM
from hardware_abstract_layer.pwm import ControlInputToPWM


class PWMManager:
    def __init__(self):
        self.PWM = PWM()

    def set_pwm_frequency(self, frequency):                # setting pwm frequecy
        self.PWM.set_frequency(frequency)

    def set_servo(self, channel, servo_name):              # setting servo name and channel
        self.PWM.set_servo(channel, servo_name)

    def get_servo_name(self, channel):                     # getting servo channel
        self.PWM.get_servo_name(channel)

    def get_servo_channel(self, servo_name):               # getting servo name
        self.PWM.get_servo_channel(servo_name)

    def set_servo_value(self, channel_name, value):        # setting servo value
        self.PWM.set_servo_value(channel_name, value)

    def set_motor(self, channel, motor_name):              # setting channel for motor
        self.PWM.set_motor(channel, motor_name)

    def get_motor_name(self, channel):                     # getting motor name
        self.PWM.get_motor_name(channel)

    def get_motor_channel(self, motor_name):               # getting motor channel
        self.PWM.get_motor_channel(motor_name)

    def set_motor_value(self, channel_name, value):        # getting motor value
        self.PWM.set_motor_value(channel_name, value)


class PWMControlManager:
    def __init__(self):
        """ Initialize all components of PWM manager"""
        self.pwm = 0
        self.ToPWM = ControlInputToPWM()

    def map_servo_mid_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 servo PWM value CENTERED"""

        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:  # subtract by mid value of the percentage
            self.pwm = self.ToPWM.bit_precision_4_mid_map(percentage, 1)
        elif bit_precision == 8:
            self.pwm = self.ToPWM.bit_precision_8_mid_map(percentage, 1)
        else:
            raise ValueError("ERROR: bit-precision not defined")
        return self.pwm

    def map_servo_full_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 motor PWM value MIN to MAX"""
        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:
            self.pwm = self.ToPWM.bit_precision_4_full_map(percentage, 1)
        elif bit_precision == 8:
            self.pwm = self.ToPWM.bit_precision_8_full_map(percentage, 1)
        else:
            raise ValueError('ERROR: bit-precision not defined')
        return self.pwm

    def map_motor_mid_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 motor PWM value CENTERED """

        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:  # subtract by mid value of the percentage
            self.pwm = self.ToPWM.bit_precision_4_mid_map(percentage, 2)
        elif bit_precision == 8:
            self.pwm = self.ToPWM.bit_precision_8_mid_map(percentage, 2)
        return self.pwm

    def map_motor_full_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 motor PWM value MIN to MAX"""
        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:
            self.pwm = self.ToPWM.bit_precision_4_full_map(percentage, 2)
        elif bit_precision == 8:
            self.pwm = self.ToPWM.bit_precision_8_full_map(percentage, 2)
        else:
            raise ValueError('ERROR: bit-precision not defined')
        return self.pwm
