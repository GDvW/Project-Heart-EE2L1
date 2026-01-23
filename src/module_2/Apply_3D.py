import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from os.path import join
from copy import deepcopy

from scipy.io import wavfile
from lib.model.Model_3D import Model_3D, Point

from lib.model.Model import Model
from lib.config.ConfigParser import ConfigParser
from lib.general.generalUtils import white_noise, write_stereo


PLOT = False


config = ConfigParser()

root = Path(join(config.TestData.SoundsPath,"Phantom"))


for sources_file in root.glob("*.wav"):
#sources_file = "generated/test data/Phantom/M-Silent.wav"

    Fs, stereo = wavfile.read(sources_file) # left: top, right: EWI tower

    left_audio = stereo[:,0]
    right_audio = stereo[:,1]

    mic_locs = [Point(-0.026052, 0.046959, 0), # 0
                Point(0.023154, 0.048927, 0), # 1
                Point(-0.025825, -0.03398, 0), # 2
                Point(0.025354, -0.02115, 0), # 3
                Point(-0.023613, -0.052407, 0), # 4
                Point(0.024461, -0.053514, 0)] # 5

    left_source_loc = Point(0,0.021307,0.079)
    right_source_loc = Point(0,-0.023562,0.079)

    model = Model_3D(config, [left_source_loc, right_source_loc], mic_locs)


    simulated_mic_recordings = model.generate([left_audio, right_audio])

    model.save(f"testdata/{sources_file.stem}")


    if PLOT:
        for i, x in enumerate(simulated_mic_recordings):
            plt.plot(x, label=f"Mic {i}")
            plt.legend()
            plt.show()