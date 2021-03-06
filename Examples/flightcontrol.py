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

TelemetryManager = telemetry.TelemetryManager()
CompressionManager = telemetry.CompressionManager()
PWMControlManager = pwm.PWMControlManager()
PWM = pwm.PWM()
InputControlManager = io.InputControlManager()

connection = TelemetryManager.initialize_server_connection(12345)
PWM.set_frequency(50)
while 1:
    compressed_inputs = TelemetryManager.receive(3, connection)
    TelemetryManager.send(bytes(1), connection)
    print(compressed_inputs)
    decompressed_inputs = CompressionManager.decompress_4_bits(compressed_inputs)
    print(decompressed_inputs)
    PWM.set_servo_value(0, PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[0], 4))
    PWM.set_servo_value(1, PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[0], 4))
    PWM.set_servo_value(2, PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[1], 4))
    print(PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[2], 4), decompressed_inputs[2])
    PWM.set_servo_value(3, PWMControlManager.map_servo_mid_range_pwm(decompressed_inputs[3], 4))
    PWM.set_motor_value(15,
                        PWMControlManager.map_motor_full_range_pwm(
                            InputControlManager.invert_controller_input(decompressed_inputs[4])
                            , 4))
    print(decompressed_inputs[5])
