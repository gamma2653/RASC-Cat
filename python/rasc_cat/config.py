import socket

CONNECTION = {
    'socket': {
        'host': ('localhost',26656),
        'args': {
            'family': socket.AddressFamily.AF_INET,
            'type': socket.SOCK_STREAM
        }
    }
}


PERSONALITY = {
    'chaos': 5.0
}

del socket