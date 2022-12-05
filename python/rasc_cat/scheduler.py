# TODO: Reimplement in C++ or Rust(preferred)

from collections import namedtuple
from typing import Iterable, Any, MutableSequence, Optional
import logging
import subprocess
from enum import Enum, auto as enum_auto
import os
from abc import ABC, abstractmethod
from contextlib import AbstractContextManager

import multiprocessing

PROJECT_NAME = 'RASC_CAT'

class System: # Note: Not a real scheduler, but needed a python based controller for testing.
    
    modules: MutableSequence[multiprocessing.Process] = []
    running: bool = False

    def __init__(self, name=PROJECT_NAME, modules: Optional[Iterable[multiprocessing.Process]] = None,
            log_level = logging.INFO, log_file='./output.log'):

        ##### Logger setup #####
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
        ##### End logger setup #####
        if modules is not None:
            self.modules.extend(modules)
        

    def add_module(self, module: multiprocessing.Process):
        self.modules.append(module)
        

    def start(self):
        self.running = True
        for module in self.modules:
            module.run()
        
    def stop(self, timeout=None):
        for module in self.modules:
            module.join(timeout)

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()