from hardware_abstract_layer import network


class TelemetryManager:
    def __init__(self):
        pass
        self.NetworkAdapter = network.NetworkAdapter()

    def initialize_server_connection(self, ip_address, port):
        """Initialize server connection by calling Network Adapter"""
        server_connection = self.NetworkAdapter.initialize_server_connection(ip_address, port)
        return server_connection

    def initialize_client_connection(self, port):
        """Initialize client connection by calling Network Adapter"""
        client_connection = self.NetworkAdapter.initialize_client_connection(port)
        return client_connection

    def send(self, data, connection):
        """Send data over network in string format"""
        return connection.send(data.encode())

    def receive(self, size, connection):
        """Receive data over network with size argument as integer defining the no. of bytes"""
        return connection.recv(size).decode()


class CompressionManager:
    def __init__(self):
        self.inverse_bit_mapping = {'0000': 0, '0001': 1, '0010': 2, '0011': 3, '0100': 4, '0101': 5, '0110': 6,
                                    '0111': 7, '1000': 8, '1001': 9, '1010': 'A', '1011': 'B', '1100': 'C', '1101': 'D',
                                    '1111': 'E'}

        self.forward_bit_mapping = {0: '0000', 1: '0001', 2: '0010', 3: '0011', 4: '0100', 5: '0101', 6: '0110',
                                    7: '0111', 8: '1000', 9: '1001', 'A': '1010', 'B': '1011', 'C': '1100', 'D': '1101',
                                    'E': '1111'}
        self.byte_string = bytes('')

    def get_byte(self, p):
        s = str(p)
        b = '0'
        if len(s) < 2:
            b += s
        else:
            b = s
        bits = (self.forward_bit_mapping[int(b[0])] + self.forward_bit_mapping[int(b[1])])
        padded_bits = bits + '0' * (8 - len(bits) % 8)
        z = list(int(padded_bits, 2).to_bytes(len(padded_bits) // 8, 'big'))
        byte = bytes([z[0]])
        return byte

    def compress_8_bits(self, inputs):
        for inp in inputs:
            self.byte_string += self.get_byte(inp)
        return self.byte_string

    def decompress_8_bits(self, inputs):
        output = []
        for inp in inputs:
            s = str(bin(ord(inp))[2:].zfill(8))
            b1 = s[:4]
            b2 = s[4:]
            p1 = str(self.inverse_bit_mapping[b1])
            p2 = str(self.inverse_bit_mapping[b2])
            output.append(int(p1+p2))
        return output








