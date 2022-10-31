# TODO: Reimplement in C++ or Rust(preferred)

from collections import namedtuple
from typing import Iterable, Any, MutableSequence
import logging
import subprocess
from enum import Enum, auto as enum_auto
import os

PROJECT_NAME = 'RASC_CAT'

class ModuleType(Enum):
    MODULE = enum_auto()
    START_SCRIPT = enum_auto()

class EnvType(Enum):
    ISOLATED = enum_auto()
    SYSTEM = enum_auto()
    CURRENT = enum_auto()

ModuleData = namedtuple('ModuleData', ('name', 'path', 'env_type', 'mod_type', 'args', 'kwargs'))
# Typing: (str, Optional[pathlib.Path], ModuleType, Iterable[Any], Iterable[Any])

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
        for mod_name, path, env_type, mod_type, args, kwargs in self.modules:
            windows_cmd = f'source {os.path.join(path, "venv", "bin", "activate")}'
            posix_cmd = f'call {os.path.join(path, "venv", "Scripts", "activate")}'
            env_activate_cmd = windows_cmd if os.name == 'nt' else posix_cmd
            start_cmd = f'python -m {mod_name}' if env_type is ModuleType.MODULE else f'python {os.path.join(path, f"{mod_name}.py")}'
            # Technically could also be 'java', but I will assume we're not running w/ Jython. :)
            subprocess.run(
                f'''{env_activate_cmd}
                python -m {mod_name}''' 
            )
        
    def stop(self):
        for module, _, _ in self.modules:
            module.stop()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()