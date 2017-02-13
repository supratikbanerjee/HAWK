import io

from manager import telemetry

TelemetryManager = telemetry.TelemetryManager()
CompressionManager = telemetry.CompressionManager()

InputControlManager = io.InputControlManager()
InputDeviceManager = io.InputDeviceManager()

# connection = TelemetryManager.initialize_server_connection(12345)

# InputDeviceManager() not sure if initialisation necessary
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
        rt = InputDeviceManager.get_r_trigger(e)
        lt = InputDeviceManager.get_l_trigger(e)
        bstate3 = InputDeviceManager.get_button_state(e, 3)
        bstate2 = InputDeviceManager.get_button_state(e, 2)

        if bstate3 == 'down':
            bY = 1
            bX = 0
        elif bstate2 == 'down':
            bX = 1
            bY = 0
        print(lx, ly, rx, rt, bX, bY)

        # CompressionManager() not sure if initialisation necessary
        mssg = CompressionManager.compress_4_bits(str(InputControlManager.input_percentage_mid_range(lx, 0.25)) + str(
            InputControlManager.input_percentage_mid_range(ly, 0.25))) + CompressionManager.compress_4_bits(
            str(InputControlManager.input_percentage_mid_range(rx, 0.25)) + str(
                InputControlManager.input_percentage_full_range(rt, 0.15))) + CompressionManager.compress_4_bits(
            str(bX) + str(bY))
        print(type(mssg))
        print(mssg)

        dmssg = CompressionManager.decompress_4_bits(mssg)
        print(dmssg)


        # TelemetryManager.send(mssg, connection)
        # TelemetryManager.receive(1, connection)
