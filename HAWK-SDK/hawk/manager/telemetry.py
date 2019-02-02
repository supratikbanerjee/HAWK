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


from hardware_abstract_layer import network
import struct


class TelemetryManager:
    def __init__(self):
        self.NetworkAdapter = network.NetworkAdapter()

    def get_ip_address(self):
        return self.NetworkAdapter.get_ip_address()

    def initialize_server_connection(self, ip_address, port):
        """Initialize server connection by calling Network Adapter"""
        server_connection = self.NetworkAdapter.initialize_server_connection(ip_address, port)
        return server_connection

    def initialize_client_connection(self, ip_address, port):
        """Initialize client connection by calling Network Adapter"""
        client_connection = self.NetworkAdapter.initialize_client_connection(ip_address, port)
        return client_connection

    def initialize_udp_connection(self):
        return self.NetworkAdapter.initialize_udp_connection()

    def bind_udp(self, connection, ip_address, port):
        return self.NetworkAdapter.bind_udp(connection, ip_address, port)

    def close(self, connection):
        return connection.close()

    def send(self, data, connection):
        """Send data over network in string format"""
        packer = struct.Struct(len(list(data))*'B')
        data = tuple(data)
        data = packer.pack(*data)
        return connection.send(data)

    def receive(self, size, connection):
        """Receive data over network with size argument as integer defining the no. of bytes"""
        unpacker = struct.Struct(size*'B')
        data = connection.recv(size)
        unpacked_data = unpacker.unpack(data)
        return unpacked_data

    def send_udp(self, data, connection, ip_address, port):
        packer = struct.Struct(len(list(data))*'B')
        data = tuple(data)
        data = packer.pack(*data)
        return connection.sendto(data, (ip_address, port))

    def receive_udp(self, size, connection):
        unpacker = struct.Struct(size * 'B')
        data, addr = connection.recvfrom(size)
        unpacked_data = unpacker.unpack(data)
        return unpacked_data

    def get_network_strength(self, network_file_linux):
        return self.NetworkAdapter.get_network_strength(network_file_linux)


class CompressionManager:
    def __init__(self):
        self.inverse_bit_mapping = {'0000': 0, '0001': 1, '0010': 2, '0011': 3, '0100': 4, '0101': 5, '0110': 6,
                                    '0111': 7, '1000': 8, '1001': 9, '1010': 10, '1011': 11, '1100': 12, '1101': 13,
                                    '1110': 14, '1111': 15}

        self.forward_bit_mapping = {0: '0000', 1: '0001', 2: '0010', 3: '0011', 4: '0100', 5: '0101', 6: '0110',
                                    7: '0111', 8: '1000', 9: '1001', 10: '1010', 11: '1011', 12: '1100', 13: '1101', 14: '1110',
                                    15: '1111'}

    def compress_4_bits(self, b1, b2):
        bit4 = 0
        if b2 == -1:
            b2 = 0
            bit4 = 1
        bits = (self.forward_bit_mapping[int(b1)] + self.forward_bit_mapping[int(b2)])
        padded_bits = bits + '0' * (8 - len(bits) % 8)
        z = list(int(padded_bits, 2).to_bytes(len(padded_bits) // 8, 'big'))
        # z = ('%%0%dx' % (len(padded_bits) // 8 << 1) % int(padded_bits, 2)).decode('hex')[-len(padded_bits) // 8:] python 2
        # byte = bytes([z[0]])
        # byte = bytes(z[0]) python 2
        # return int(z[0].encode('hex'), 16) python 2
        if bit4 == 1:
            return bits
        return int(z[0])

    def decompress_4_bits(self, o):
        output = []
        s = str(bin(int(str(o), base=10))[2:].zfill(8))
        b1 = s[:4]
        b2 = s[4:]
        p1 = str(self.inverse_bit_mapping[b1])
        p2 = str(self.inverse_bit_mapping[b2])
        # print('Decompressing ',p1,p2)
        output.append(int(p1))  # need to change return type
        output.append(int(p2))  # need to change return type
        return output
