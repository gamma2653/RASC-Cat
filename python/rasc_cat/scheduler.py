# TODO: Reimplement in C++ or Rust(preferred)

import pathlib
from collections import namedtuple
from typing import Iterable, Any, MutableSequence
import logging
import subprocess


PROJECT_NAME = 'RASC_CAT'

ModuleData = namedtuple('ModuleData', ('name', 'path'))
# Typing: (str, pathlib.Path)

class System: # Note: Not a real scheduler, but needed a python based controller for testing.
    
    modules: MutableSequence[ModuleData] = []

    def __init__(self, name=PROJECT_NAME, log_level = logging.INFO, log_file='./output.log'):

        # Logger setup
        formatter = logging.Formatter('[%(asctime)s] [%(name)s]: [%(levelname)s] %(message)s',
                                        datefmt='%m-%d-%Y %H:%M:%S')
        
        self.logger = logging.getLogger(name)
        self.logger.setLevel(log_level)

        # Add console handler
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        self.logger.addHandler(console_handler)

        # Add file handler if log file is being kept.
        if log_file is not None:
            file_handler = logging.FileHandler(log_file)
            file_handler.setFormatter(formatter)
            self.logger.addHandler(file_handler)

    def add_module(self, module: ModuleData, args: Iterable[Any] = (), kwargs: Iterable[Any] = ()):
        self.modules.append(module, args, kwargs)

    def start(self):
        for module, args, kwargs in self.modules:
            subprocess.run()
            module.start(*args, **kwargs)
        
    def stop(self):
        for module, _, _ in self.modules:
            module.stop()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()