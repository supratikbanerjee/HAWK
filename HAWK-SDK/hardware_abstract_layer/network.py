import socket
'''Network Adapter wrapper around python for managing proper network communication'''


class NetworkAdapter:
    def __init__(self):
        self.IP = socket.gethostbyname(socket.gethostname())
        self.port = 12345

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






