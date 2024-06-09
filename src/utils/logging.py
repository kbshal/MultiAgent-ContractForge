import logging
import sys

class AgentLogger(logging.Logger):
    def __init__(self, name='root', level=logging.NOTSET, stream=sys.stdout, format=None, datefmt=None, style='%'):
        super().__init__(name, level)
        ch = logging.StreamHandler(stream)
        formatter = logging.Formatter(format, datefmt, style)
        ch.setFormatter(formatter)
        self.addHandler(ch)
        self.setLevel(level)
        self.propagate = False