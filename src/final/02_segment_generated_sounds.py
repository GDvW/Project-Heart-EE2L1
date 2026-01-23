from lib.config.ConfigParser import ConfigParser
from lib.processing.Executor import Executor

def main():
    """
    @author: Gerrald
    @date: 23/01/2026
    """
    config = ConfigParser()
    executor = Executor("generated\\hearbeat model\\3d-model\\HeartSimulation", config, output_subfolder="3D model heartsimulation", log=True)
    executor.execute()
    executor.summarize()

if __name__ == "__main__":
    main()