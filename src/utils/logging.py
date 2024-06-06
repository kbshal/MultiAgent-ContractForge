from loguru import logger


class AgentLogger(logger):
   def __init__(self, record=None, lazy=False, colors=True, raw=False, capture=False, patchers=None, extra=None):
        super().__init__(record=record, lazy=lazy, colors=colors, raw=raw, capture=capture, patchers=patchers, extra=extra)

        self.level("DEBUG_INFO", no=15)

        self.add("contractagent.log", level="DEBUG_INFO")