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


from hawk.manager import io
from hawk.manager import telemetry
from hawk.manager import pwm
from hardware_abstract_layer.sensors import barometer
from ina219 import INA219

# from hardware_abstract_layer.sensors import gyroscope

# MPU6050 = gyroscope.MPU6050()
BMP280 = barometer.BMP280()
TelemetryManager = telemetry.TelemetryManager()
CompressionManager = telemetry.CompressionManager()
PWMControlManager = pwm.PWMControlManager()
PWM = pwm.PWM()
SHUNT_OHMS = 0.1
MAX_EXPECTED_AMPS = 0.1
ina = INA219(SHUNT_OHMS, MAX_EXPECTED_AMPS, address=0x44)
ina.configure(ina.RANGE_16V)
InputControlManager = io.InputControlManager()
ip = TelemetryManager.get_ip_address()
connection = TelemetryManager.initialize_server_connection(ip, 12345)
PWM.set_frequency(50)
active = True
bit = 8
telemetry_data = [0] * 4
base_pressure = BMP280.read_pressure()
cell = 3
min_voltage = 3.5
max_volts = cell * 4.2
min_volts = min_voltage * cell
engine_hold = 0
while active:
    # signal = int(TelemetryManager.get_network_strength('/proc/net/wireless')/10)
    altitude = BMP280.read_altitude(base_pressure)
    temperature = BMP280.read_temperature()
    bus_voltage = ina.voltage()
    volts_range = max_volts - min_volts
    volts = bus_voltage - min_volts
    volts_percent = (volts/volts_range) * 100
    '''x_angle, y_angle = MPU6050.get_angles()
    x = int(x_angle/10)
    y = int(y_angle/10)
    if -6 < y < 6:
        if y < 0:
            y = 5 + (-1*y)
    else:
        y = 0

    if -6 < x < 6:
        if x < 0:
            x = 5 + (-1*x)
    else:
        x = 0
    telemetry_data[0] = CompressionManager.compress_4_bits(x, y) #) # linux'''
    telemetry_data[0] = int(TelemetryManager.get_network_strength('/proc/net/wireless'))
    telemetry_data[1] = int(volts_percent)
    telemetry_data[2] = int(altitude)
    telemetry_data[3] = int(temperature)

    compressed_inputs = TelemetryManager.receive(6, connection)
    TelemetryManager.send(telemetry_data, connection)
    #aileron = compressed_inputs[0]#CompressionManager.decompress_8_bits(compressed_inputs[0])
    #elevator = compressed_inputs[1] #CompressionManager.decompress_8_bits(compressed_inputs[1])
    #rudder = compressed_inputs[2]#CompressionManager.decompress_8_bits(compressed_inputs[2])
    #throttle = compressed_inputs[3]#CompressionManager.decompress_8_bits(compressed_inputs[3])
    #print(compressed_inputs[4])
    control_surface = list(compressed_inputs)
    bxby = CompressionManager.decompress_4_bits(control_surface[4])
    babb = CompressionManager.decompress_4_bits(control_surface[5])
    bX = bxby[0]
    bY = bxby[1]
    bA = babb[0]
    bB = babb[1]
    print(control_surface[0], control_surface[1], control_surface[2], control_surface[3], bX, bY, bA, bB)
    # print(decompressed_inputs)
    PWM.set_servo_value(0, PWMControlManager.map_servo_mid_range_pwm(control_surface[0], 8))
    PWM.set_servo_value(1, PWMControlManager.map_servo_mid_range_pwm(control_surface[0], 8))
    PWM.set_servo_value(2, PWMControlManager.map_servo_mid_range_pwm(control_surface[1], 8))
    # print(PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[2], 4), decompressed_inputs[2])
    PWM.set_servo_value(3, PWMControlManager.map_servo_mid_range_pwm(control_surface[2], 8))
    if bB == 1:
        if bX == 1:
            PWM.set_motor_value(15,
                                PWMControlManager.map_motor_full_range_pwm(
                                    InputControlManager.invert_controller_input(engine_hold, 8)
                                    , 8))
        else:
            engine_hold = control_surface[3]
            PWM.set_motor_value(15,
                                PWMControlManager.map_motor_full_range_pwm(
                                    InputControlManager.invert_controller_input(engine_hold, 8)
                                    , 8))
    else:
        PWM.set_motor_value(15, PWMControlManager.map_motor_full_range_pwm(InputControlManager.invert_controller_input(10, 4), 8))

    if bY == 1:
        PWM.set_servo_value(0, PWMControlManager.map_servo_mid_range_pwm(5, 4))
        PWM.set_servo_value(1, PWMControlManager.map_servo_mid_range_pwm(5, 4))
        PWM.set_servo_value(2, PWMControlManager.map_servo_mid_range_pwm(5, 4))
        PWM.set_servo_value(3, PWMControlManager.map_servo_mid_range_pwm(5, 4))
        PWM.set_motor_value(15, PWMControlManager.map_motor_full_range_pwm(InputControlManager.invert_controller_input(10, 4), 4))
        active = False
TelemetryManager.close(connection)
# print(PWMControlManager.map_motor_full_range_pwm(
#                        InputControlManager.invert_controller_input(decompressed_inputs[3])
#                        , 4))
# print(decompressed_inputs[4], decompressed_inputs[5])
