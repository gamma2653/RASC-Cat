import multiprocessing
import threading

from rasc_cat import config


class Module(multiprocessing.Process):
    socket = socket.socket(**config.Connection['socket']['args'])
    input_thread = threading.Thread(target=self._accept_cmd)
    data_buffer = []

    def __init__(self, module_name='Unnamed Module'):
        super().__init__()
        self.name = module_name
        self.socket.connect(config.CONNECTION['socket']['host'])
        self.socket.sendall(f'["connected","{module_name}"]'.encode('utf-8'))
    
    def _accept_cmd(self):
        """
        Should only be running in one thread per Module.

        Reads data from socket and stores it in `data_buffer`.
        """

        def take_data(buff = ''):
            while ']' not in buff:
                data = self.socket.recv(1024)
                buff += data.decode()
            buff = buff.trim()
            # Extract command
            left, right = buff.index('['), buff.index(']')
            while left>right:
                print('Error: broken pipe: ignoring, cleaning, and attempting to continue.')
                buff = buff[buff.index('['):]
                left, right = buff.index('['), buff.index(']')
            cmd = buff[left+1:right].split(',')
            data_buffer.append(cmd)
            # Extract rest
            leftovers = buff[buff.index(']')+1:]
            try:
                take_data(leftovers)
            except RecursionError:
                print('Hit recursion limit, to keep data integrity throwing out current data...')
                return
        
        while True:
            take_data()
        

    def communicate(self, message):
        # Correct way:
        # self.socket.sendall(f"[{','.join(message.split(' '))}]".encode('utf-8'))
        # Readable way:
        self.socket.sendall(str(list(message.split(''))).encode('utf-8'))

    
    def 

class FacialModule(Module):
    pass

class VoiceModule(Module):
    pass