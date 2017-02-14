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


from manager import io
from manager import telemetry
from manager import pwm

TelemetryManager = telemetry.TelemetryManager()
CompressionManager = telemetry.CompressionManager()
InputControlManager = io.InputControlManager()
InputDeviceManager = io.InputDeviceManager()
PWMControlManager = pwm.PWMControlManager()

ip = str(input('Enter HAWK-OS IP'))
connection = TelemetryManager.initialize_client_connection(ip, 12345)
j = InputDeviceManager.get_device()
print("joystick detected", j)
bX = 0
bY = 0

while 1:
    for e in InputDeviceManager.get_event():
        lx = InputDeviceManager.get_l_x_axis(e)
        ly = InputDeviceManager.get_l_y_axis(e)
        rx = InputDeviceManager.get_r_x_axis(e)
        ry = InputDeviceManager.get_r_y_axis(e)
        bt = InputDeviceManager.get_triggers(e)
        bstate3 = InputDeviceManager.get_button_state(e, 3)
        bstate2 = InputDeviceManager.get_button_state(e, 2)

        if bstate3 == 'down':
            bY = 1
            bX = 0
        if bstate2 == 'down':
            bX = 1
            bY = 0
        print(lx, ly, rx, bt, ry, bY)

        compressed_inputs = CompressionManager.compress_4_bits(str(InputControlManager.input_percentage_mid_range(lx, 0.25)) + str(
            InputControlManager.input_percentage_mid_range(ly, 0.25))) + CompressionManager.compress_4_bits(
            str(InputControlManager.input_percentage_mid_range(rx, 0.25)) + str(
                InputControlManager.input_percentage_mid_range(bt, 0.15))) + CompressionManager.compress_4_bits(
            str(InputControlManager.input_percentage_mid_range(ry, 0.25)) + str(bY))
        print(type(compressed_inputs))
        print(compressed_inputs)

        TelemetryManager.send(compressed_inputs, connection)
        TelemetryManager.receive(1, connection)