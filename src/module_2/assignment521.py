import numpy as np
from lib.config.ConfigParser import ConfigParser
from copy import deepcopy
import matplotlib.pyplot as plt
from lib.model.generate import *
from lib.model.Model_3D import Model_3D
import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from pathlib import Path
from scipy.io.wavfile import write

from lib.model.Model_3D import Model_3D, Point
from lib.config.ConfigParser import ConfigParser
from lib.model.Model import Model
from lib.plot.timeFrequencyPlot import timeFrequencyPlot







if __name__ == "__main__":
    config = ConfigParser()
    Fs = config.HeartSoundModel.Fs

    model = Model(config, randomize_enabled=True)
    model.import_csv(".\\src\\module_2\\model_params.csv")
    model.set_n(20)
    #model.randomize_enabled = True

    t, h = model.generate_model()

    fig, ax = plt.subplots(1, 1, figsize=(8, 4), constrained_layout=True)

    timeFrequencyPlot(h,48000,ax, None,apply_fftshift=True)

    write("./generated/segment_model.wav", 48000, h)
