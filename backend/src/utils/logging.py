import logging
import sys
import os

import logging

class AgentLogger(logging.Logger):
    def __init__(self, name='root', level=logging.NOTSET, logfile='logs/agent_logs.log', format=None, datefmt=None, style='%'):
        super().__init__(name, level)
        
        ch = logging.FileHandler(logfile)
        stream_handler = logging.StreamHandler(sys.stdout)
        os.makedirs(os.path.dirname(logfile), exist_ok=True)
        
        file_handler = logging.FileHandler(logfile)
        handlers = [file_handler, stream_handler]
        
        for handler in handlers:
            if format is None:
                format = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
                
            formatter = logging.Formatter(format, datefmt, style)
            handler.setFormatter(formatter)
            self.addHandler(handler)
        
        self.setLevel(level)
        self.propagate = False