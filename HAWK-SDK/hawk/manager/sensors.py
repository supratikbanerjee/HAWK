from hardware_abstract_layer.sensors import gyroscope


class gyroscope:
    def __init__(self):
        self.gyro = 'MPU'

    def get_sensor(self, sensor_name):
        sensor_class = sensor_name
        sensor = getattr("gyroscope", sensor_name)
        return sensor
