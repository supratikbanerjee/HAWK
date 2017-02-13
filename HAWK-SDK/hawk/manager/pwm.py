from hardware_abstract_layer.pwm import PWM
from hardware_abstract_layer.pwm import ControlInputToPWM


class PWMManager:
    def __init__(self):
        self.PWM = PWM()

    def set_pwm_frequency(self, frequency):
        self.PWM.set_frequency(frequency)

    def set_servo(self, channel, servo_name):
        self.PWM.set_servo(channel, servo_name)

    def get_servo_name(self, channel):
        self.PWM.get_servo_name(channel)

    def get_servo_channel(self, servo_name):
        self.PWM.get_servo_channel(servo_name)

    def set_servo_value(self, channel_name, value):
        self.PWM.set_servo_value(channel_name, value)

    def set_motor(self, channel, motor_name):
        self.PWM.set_motor(channel, motor_name)

    def get_motor_name(self, channel):
        self.PWM.get_motor_name(channel)

    def get_motor_channel(self, motor_name):
        self.PWM.get_motor_channel(motor_name)

    def set_motor_value(self, channel_name, value):
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
        return self.pwm

    def map_motor_full_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 motor PWM value MIN to MAX"""
        x = self.ToPWM.motor_mid
        y = 0
        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:
            y = self.ToPWM.motor_range * (percentage / 9.)  # divide by 9 to keep 4-bit precision range
        elif bit_precision == 8:
            y = self.ToPWM.motor_range * (percentage / 99.)  # divide by 99 to keep 8-bit precision range

        return int(x + y)

    def map_motor_med_range_pwm(self, percentage, bit_precision):
        """ map the input percentage to PCA9685 motor PWM value CENTERED """

        ''' 4-bit precision ranges from 1-9 and 8-bit ranges 1-99 '''
        if bit_precision == 4:  # subtract by mid value of the percentage
            self.pwm = self.ToPWM.bit_precision_4_mid_map(percentage, 2)
        elif bit_precision == 8:
            self.pwm = self.ToPWM.bit_precision_8_mid_map(percentage, 2)

        return self.pwm

