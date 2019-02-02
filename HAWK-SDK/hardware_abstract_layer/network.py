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


import socket

# import struct
'''Network Adapter wrapper around python for managing proper network communication'''


class NetworkAdapter:
    def __init__(self):
        self.IP = '10.243.34.106'
        self.port = 12345
        self.network_file_linux = '/proc/net/wireless'

    def get_ip_address(self):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        self.IP = s.getsockname()[0]
        s.close()
        return self.IP

    def initialize_server_connection(self, ip_address, port):
        """Initializing Server connection"""
        self.port = port
        address = (ip_address, self.port)
        server_socket = socket.socket()
        server_socket.bind(address)
        server_socket.listen(1)
        connection, address = server_socket.accept()
        return connection

    def initialize_client_connection(self, ip_address, port):
        """Initializing Client connection"""
        self.port = port
        client_socket = socket.socket()
        client_socket.connect((ip_address, port))
        return client_socket

    def initialize_udp_connection(self):
        return socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    def bind_udp(self, connection, ip_address, port):
        return connection.bind((ip_address, port))

    def get_network_strength(self, network_file_linux):
        self.network_file_linux = network_file_linux
        file = open(self.network_file_linux, 'r')
        line = file.readlines()
        tl = []
        for i in line:
            tl = i.split(" ")
        if tl[6] == '':
            network_strength = tl[7]
        else:
            network_strength = tl[6]
        print(network_strength)
        return int(network_strength[:-1])
