from lib.model.Model_3D import Model_3D, Point
from lib.general.generalUtils import white_noise
from lib.config.ConfigParser import ConfigParser
import numpy as np
import matplotlib.pyplot as plt

SIGNAL_LENGTH = 0.25 #seconds
SAVE = True
PLOT = False

def main():
    config = ConfigParser()
    Fs = config.HeartSoundModel.Fs
    
    signal1 = white_noise(SIGNAL_LENGTH, Fs)
    signal2 = white_noise(SIGNAL_LENGTH, Fs)
    mic_locs = [Point(-0.25, 0, 0), # 0
                Point(-0.15, 0, 0), # 1
                Point(-0.05, 0, 0), # 2
                Point(0.05, 0, 0), # 3
                Point(0.15, 0, 0), # 4
                Point(0.25, 0, 0)]
    source_loc = [Point(-1,8,-15),
                  Point(3,7,0)]
    
    model = Model_3D(config, source_loc, mic_locs)
    
    h = model.generate([signal1, signal2])
    
    if PLOT:
        for i, x in enumerate(h):
            plt.plot(x, label=f"Mic {i}")
        plt.legend()
        plt.show()
    if SAVE:
        model.save("White Noise")

    

if __name__ == "__main__":
    main()