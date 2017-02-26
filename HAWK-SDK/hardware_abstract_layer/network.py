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
#import struct
'''Network Adapter wrapper around python for managing proper network communication'''


class NetworkAdapter:
    def __init__(self):
        self.IP = '192.168.0.110'
        self.port = 12345

    '''def get_ip_address(self, ifname):
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        return socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])'''

    def initialize_server_connection(self, port):
        """Initializing Server connection"""
        self.port = port
        address = (self.IP, self.port)
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
