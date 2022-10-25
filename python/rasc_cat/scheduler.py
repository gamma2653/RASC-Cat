# TODO: Reimplement in C++ or Rust(preferred)

from typing import Protocol, Iterable, Any, MutableSequence
from abc import abstractmethod
import logging


PROJECT_NAME = 'RASC_CAT'


class Module(Protocol):
    """
    Contains the methods: `start`, `stop`, and `run` method.
    """

    @abstractmethod
    def start(self):
        pass

    @abstractmethod
    def stop(self):
        pass

    @abstractmethod
    def run(self):
        pass


class System: # Note: Not a real scheduler, but needed a controller.
    
    modules: MutableSequence[Module] = []

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

    def add_module(self, module: Module, args: Iterable[Any] = (), kwargs: Iterable[Any] = ()):
        self.modules.append(module, args, kwargs)

    def start(self):
        for module, args, kwargs in self.modules:
            module.start(*args, **kwargs)
        
    def stop(self):
        for module, _, _ in self.modules:
            module.stop()

    def __enter__(self):
        self.start()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()