from loguru import logger


class AgentLogger(logger):
    def __init__(self):
        super().__init__()

        self.level("DEBUG_INFO", no=15)

        self.add("contractagent.log", level="DEBUG_INFO")