from lib.config.ConfigParser import ConfigParser
from lib.processing.Executor import Executor

config = ConfigParser()

executor = Executor("samples\\stethoscope_2_realHeart_", config, True)
executor.execute()
executor.summarize()


