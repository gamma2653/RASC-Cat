import socket

CONNECTION = {
    'socket': {
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