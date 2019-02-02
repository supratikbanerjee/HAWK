from hardware_abstract_layer.sensors import smbus
import math


class MPU6050:
    def __init__(self):
        # Power management registers
        self.power_mgmt_1 = 0x6b
        self.power_mgmt_2 = 0x6c
        self.bus = smbus.SMBus(1)
        self.address = 0x68  # This is the address value read via the i2cdetect command
        # Now wake the 6050 up as it starts in sleep mode
        self.bus.write_byte_data(self.address, self.power_mgmt_1, 0)

    def read_byte(self, adr):
        return self.bus.read_byte_data(self.address, adr)

    def read_word(self, adr):          # reads raw accelerometer data
        high = self.bus.read_byte_data(self.address, adr)
        low = self.bus.read_byte_data(self.address, adr + 1)
        val = (high << 8) + low
        return val

    def read_word_2c(self, adr):            #reads a word (16 bits) from a given register and converts it from two's complement
        val = self.read_word(adr)
        if val >= 0x8000:
            return -((65535 - val) + 1)
        else:
            return val

    def dist(self, a, b):
        return math.sqrt((a * a) + (b * b))

    def get_y_rotation(self, x, y, z):                   #getting the degree of rotation about y axis in degrees
        radians = math.atan2(x, self.dist(y, z))
        return -math.degrees(radians)

    def get_x_rotation(self, x, y, z):                   #getting the degree of rotation about x axis in degrees
        radians = math.atan2(y, self.dist(x, z))
        return math.degrees(radians)

    def get_angles(self):
        # print "gyro data"
        # print "---------"
        # gyro_xout = read_word_2c(0x43)
        # gyro_yout = read_word_2c(0x45)
        # gyro_zout = read_word_2c(0x47)
        # print "gyro_xout: ", gyro_xout, " scaled: ", (gyro_xout / 131)
        # print "gyro_yout: ", gyro_yout, " scaled: ", (gyro_yout / 131)
        # print "gyro_zout: ", gyro_zout, " scaled: ", (gyro_zout / 131)
        # print
        # print("accelerometer data"
        # print "------------------"
        accel_xout = self.read_word_2c(0x3b)
        accel_yout = self.read_word_2c(0x3d)
        accel_zout = self.read_word_2c(0x3f)
        accel_xout_scaled = accel_xout / 16384.0
        accel_yout_scaled = accel_yout / 16384.0
        accel_zout_scaled = accel_zout / 16384.0
        #
        # print "accel_xout: ", accel_xout, " scaled: ", accel_xout_scaled
        # print "accel_yout: ", accel_yout, " scaled: ", accel_yout_scaled
        # print "accel_zout: ", accel_zout, " scaled: ", accel_zout_scaled
        xr = self.get_x_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        yr = self.get_y_rotation(accel_xout_scaled, accel_yout_scaled, accel_zout_scaled)
        return xr, yr
