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

import time
from hawk.manager import io
from hawk.manager import telemetry
from hawk.manager import pwm
from groundstation import groundstation_ui as ui
from groundstation import groundstation_config as config
from groundstation import constants as const

active = True
TelemetryManager = telemetry.TelemetryManager()
CompressionManager = telemetry.CompressionManager()
InputControlManager = io.InputControlManager()
InputDeviceManager = io.InputDeviceManager()
PWMControlManager = pwm.PWMControlManager()

ip_address = str(input('Enter HAWK-OS IP: '))
port = 12345
connection = TelemetryManager.initialize_client_connection(ip_address, port)
#connection = TelemetryManager.initialize_udp_connection()
j = InputDeviceManager.get_device()
print("joystick detected", j)

dr = 0
expo = 0
bit = 0

if bit == 4:
    max_input = 10
    mid_input = 5
    norm = 1
else:
    max_input = 255
    mid_input = 127
    norm = 25

compressed_inputs = bytes(0)
update_time_start = time.time()
elapsed_time = 0
bX_Active = False
bY_Active = False
bA_Active = False
bB_Active = False
latency = 0
control_surface = [0]*6
bX = 0
bY = 0
bA = 0
bB = 0
LB = 0
RB = 0
dpad = 0
page = 1
page_max =2
dr_expo_set = 0
dr_expo_step = 5
dr_expo_set_max = 3
min_ms = 100
max_ms = 0
avg_ms = 0
count_ms = 0


def update():
    global update_time_start, elapsed_time, bX_Active, bY_Active, latency, control_surface, bX, bY, compressed_inputs, \
        active, expo, dr, bit, bA, bB, bA_Active, bB_Active, dpad, page, LB, RB, page_max, dr_expo_set, \
        dr_expo_step, dr_expo_set_max, min_ms, max_ms, avg_ms, count_ms
    for e in InputDeviceManager.get_event():
        # InputDeviceManager.input_wait()
        lx = InputDeviceManager.get_l_x_axis(e)
        ly = InputDeviceManager.get_l_y_axis(e)
        rx = InputDeviceManager.get_r_x_axis(e)
        ry = InputDeviceManager.get_r_y_axis(e)
        bt = InputDeviceManager.get_triggers(e)
        bstate5 = InputDeviceManager.get_button_state(e, 5)
        bstate4 = InputDeviceManager.get_button_state(e, 4)
        bstate3 = InputDeviceManager.get_button_state(e, 3)
        bstate2 = InputDeviceManager.get_button_state(e, 2)
        bstate1 = InputDeviceManager.get_button_state(e, 1)
        bstate0 = InputDeviceManager.get_button_state(e, 0)
        dpad = InputDeviceManager.get_dpad(e)

        if bstate3 == 'down':
            bY_Active = not bY_Active
            if bY_Active:
                bY = 1
            else:
                bY = 0
        if bstate2 == 'down':
            bX_Active = not bX_Active
            if bX_Active:
                bX = 1
            else:
                bX = 0

        if bstate0 == 'down':
            bA_Active = not bA_Active
            if bA_Active:
                bA = 1
            else:
                bA = 0
        if bstate1 == 'down':
            bB_Active = not bB_Active
            if bB_Active:
                bB = 1
            else:
                bB = 0
        if bstate4 == 'down':
            LB = 1
            RB = 0

        if bstate5 == 'down':
            RB = 1
            LB = 0

        if bY == 1:
            active = False
        if LB == 1:
            if page > 1:
                page -= 1
        if RB == 1:
            if page < page_max:
                page += 1

        if page == 1:
            if dpad == 1:
                if dr_expo_set < dr_expo_set_max:
                    dr_expo_set += 1
            elif dpad == 3:
                if dr_expo_set > 0:
                    dr_expo_set -= 1
            if dpad == 2:
                if dr_expo_set == 0:
                    if expo < 100:
                        expo += dr_expo_step
                elif dr_expo_set == 1:
                    if dr < 100:
                        dr += dr_expo_step
                elif dr_expo_set == 2:
                    if dr_expo_step < 100:
                        dr_expo_step += 1
            elif dpad == 4:
                if dr_expo_set == 0:
                    if expo > 0:
                        expo -= dr_expo_step
                elif dr_expo_set == 1:
                    if dr > 0:
                        dr -= dr_expo_step
                elif dr_expo_set == 2:
                    if dr_expo_step > 0:
                        dr_expo_step -= 1
            config.write_config(expo, dr, bit)

        control_surface[0] = int(InputControlManager.input_percentage_mid_range(InputControlManager.set_exponential_dual_rate(expo, dr, rx),
                                                                                0.15, bit))
        control_surface[1] = int(InputControlManager.input_percentage_mid_range(InputControlManager.set_exponential_dual_rate(expo, dr, ry),
                                                                                0.15, bit))
        # print(control_surface[1], InputControlManager.input_percentage_mid_range(ry, 0.1, bit), expo,
        #      InputControlManager.set_exponential_dual_rate(expo, dr, ry), ry)
        # InputControlManager.input_percentage_mid_range(lx, 0.25)
        control_surface[2] = InputControlManager.input_percentage_mid_range(bt, 0.1, bit)
        control_surface[3] = InputControlManager.input_percentage_mid_range(ly, 0.2, bit)

        if bit == 4:
            control_surface[0] = CompressionManager.compress_4_bits(control_surface[0], control_surface[1])
            control_surface[1] = CompressionManager.compress_4_bits(control_surface[2], control_surface[3])
            control_surface[2] = CompressionManager.compress_4_bits(bX, bY)
            control_surface = control_surface[:control_surface[2]]
        else:
            control_surface[4] = CompressionManager.compress_4_bits(bX, bY)
            control_surface[5] = CompressionManager.compress_4_bits(bA, bB)

        # print(control_surface[0], control_surface[1], control_surface[2], control_surface[3], bX, bY)

    t1 = time.time()
    TelemetryManager.send(control_surface, connection)
    telemetry_data = TelemetryManager.receive(4, connection)
    #TelemetryManager.send_udp(control_surface, connection, ip_address, port)
    #telemetry_data = TelemetryManager.receive_udp(5, connection)
    # telemetry_data = [0,0,0,0]
    t2 = time.time()
    if elapsed_time >= 1:
        update_time_start = time.time()
        latency = (t2-t1)*1000
        if latency < min_ms:
            min_ms = latency
        if latency > max_ms:
            max_ms = latency
        avg_ms += latency
        count_ms += 1
    update_time_stop = time.time()
    elapsed_time = update_time_stop - update_time_start
    # gyro = CompressionManager.decompress_4_bits(telemetry_data[0])
    signal = int(telemetry_data[0])
    dbm = const.cisco_dbm_dict[signal]
    '''angle_h, horizontal_angle = ui.get_horizontal_angle(gyro[1])
    if angle_h > 0:
        orientation_h = 'Left'
    else:
        angle_h *= -1
        orientation_h = 'Right'
    angle_v, vertical_angle = ui.get_vertical_angle(gyro[0])
    if angle_v < 6:
        orientation_v = 'Up'
    else:
        angle_v *= -1
        orientation_v = 'Down'''
    battery = telemetry_data[1]
    battery_percent = battery
    battery /= 100
    battery *= (12.6 - 10.5)
    battery += 10.5
    altitude = telemetry_data[2]
    temperature = telemetry_data[3]
    ui.clear()
    ui.hawk_banner(2)
    ui.print_ui(altitude, temperature, dr_expo_step, expo, dr, page, bY, bB, bX, bA, dbm, battery_percent, battery, signal, latency,
                control_surface[0],
                norm,
                max_input,
                mid_input, control_surface[1],
                control_surface[2],
                InputControlManager.invert_controller_input(control_surface[3], 8))
                #horizontal_angle, vertical_angle, angle_v, orientation_v, angle_h, orientation_h)


while active:
    conf = config.read_config()
    expo = conf['expo']
    dr = conf['dr']
    bit = conf['bit']
    update()
TelemetryManager.close(connection)
avg_ms /= count_ms
print('Min Latency:', min_ms)
print('Max Latency:', max_ms)
print('Average Latency:', avg_ms)


