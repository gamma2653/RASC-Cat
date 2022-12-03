import socket
import requests
from enum import IntFlag
from queue import PriorityQueue
from typing import Tuple

from rasc_cat import scheduler, config

class ConnectionType(IntFlag):
    NONE = 0b00
    HTTP = 0b01
    SOCK = 0b10
    FULL = 0b11

class Connection:

    def __init__(self, mod_name: str, ip: str, port: int, conn_type: ConnectionType):
        self.mod_name, self.ip, self.port, self.conn_type = mod_name, ip, port, conn_type
        self.set_http_addr(ip, port)
        self.sockets: PriorityQueue[Tuple[int, socket.socket]]


    def connect(self):
        if self.conn_type & ConnectionType.SOCK:
            sock = socket.socket(**config.CONNECTION['socket']['args'])
            sock.connect((self.ip, self.port))
            self.sockets.put((0, sock))
        if self.conn_type & ConnectionType.HTTP:
            # 
            requests.get(self.http_addr + '/checkin', {
                'module': self.mod_name
            })

    def __enter__(self):
        self.connect()
    
    def disconnect(self):
        if self.conn_type & ConnectionType.SOCK:
            for sock in self.sockets:
                sock.close()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.disconnect()
        return self
    
    def set_http_addr(self, ip: str, port: int):
        self.ip, self.port = ip, port
        self.http_addr = ('' if self.port is None else f'{self.ip}' + f':{self.port}')
        prio, sock = self.sockets.get()
        self.sockets.put((prio+1, sock))
    
    '''
    API for sending data to the scheduler. Uses sockets.
    '''
    def send(self, data: bytes):
        
        pass

    '''
    API for receiving data from the scheduler. Uses sockets.
    '''
    def recv(self):
        pass

    '''
    API for requesting data from the scheduler. Uses HTTP.
    '''
    def request(self, params):
        pass

handler_data = scheduler.ModuleData('connection_handler', )