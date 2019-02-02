class SMBus(object):
    """SMBus([bus]) -> SMBus
    Return a new SMBus object that is (optionally) connected to the
    specified I2C device interface.
    """

    def __init__(self, bus):
        pass

    def close(self):
        pass

    def dealloc(self):
        pass

    def open(self, bus):
        pass

    def _set_addr(self, addr):
        pass

    # @validate(addr=int)
    def write_quick(self, addr):
        pass

    # @validate(addr=int)
    def read_byte(self, addr):
        pass

    # @validate(addr=int, val=int)
    def write_byte(self, addr, val):
        pass

    # @validate(addr=int, cmd=int)
    def read_byte_data(self, addr, cmd):
        pass

    # @validate(addr=int, cmd=int, val=int)
    def write_byte_data(self, addr, cmd, val):
        pass

    # @validate(addr=int, cmd=int)
    def read_word_data(self, addr, cmd):
        pass

    # @validate(addr=int, cmd=int, val=int)
    def write_word_data(self, addr, cmd, val):
        pass

    # @validate(addr=int, cmd=int, val=int)
    def process_call(self, addr, cmd, val):
        pass

    # @validate(addr=int, cmd=int)
    def read_block_data(self, addr, cmd):
        pass

    # @validate(addr=int, cmd=int, vals=list)
    def write_block_data(self, addr, cmd, vals):
        pass

    # @validate(addr=int, cmd=int, vals=list)
    def block_process_call(self, addr, cmd, vals):
        pass

    # @validate(addr=int, cmd=int, len=int)
    def read_i2c_block_data(self, addr, cmd, len=32):
        pass

    # @validate(addr=int, cmd=int, vals=list)
    def write_i2c_block_data(self, addr, cmd, vals):
        pass

    # @property
    def pec(self):
        pass

    # @pec.setter
    def pec(self, value):
        pass

def smbus_data_to_list(data):
    pass


def list_to_smbus_data(data, vals):
    pass
