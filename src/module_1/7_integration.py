import numpy as np
import matplotlib.pyplot as plt
from lib.plot.timeFrequencyPlot import *
from lib.plot.frequencyUtils import getDamping
from lib.general.generalUtils import todB
from lib.config.ConfigParser import ConfigParser
from lib.processing.functions import construct_bandpass_filter
from lib.processing.Processor import Processor

def assignment471(config):
    pass


def main():
    """The main loop. Can be changed to choose whether to run assignment 4.2.2 or 4.2.3.
    """
    config = ConfigParser()
    assignment471(config)

if __name__ == "__main__":
    main()