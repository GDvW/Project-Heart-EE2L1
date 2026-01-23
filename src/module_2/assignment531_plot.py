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

from lib.model.Model_3D import Model_3D, Point
from lib.config.ConfigParser import ConfigParser
from lib.model.Model import Model



plt.rcParams.update({'font.size': 30})


def plot(signals, Fs):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    for i, signal in enumerate(signals):
        t = np.linspace(0, len(signal)/Fs, len(signal))
        plt.plot(t, signal, label=f"Mic {i}")
    plt.legend(loc="best")
    plt.xlabel("Time (s)")
    plt.ylabel("Amplitude (relative)")
    plt.grid()
    plt.legend(fontsize=20)
    plt.show()


if __name__ == "__main__":
    config = ConfigParser()
    Fs = config.HeartSoundModel.Fs

    model = Model(config, randomize_enabled=False, simulate_S2=True)
    model.import_csv(".\\src\\module_2\\model_params.csv")
    model.set_n(5)
    model.randomize_enabled = True
    mic_locs = [Point(2.5, 5, 0), # 0
                Point(2.5, 10, 0), # 1
                Point(2.5, 15, 0), # 2
                Point(7.5, 5, 0), # 3
                Point(7.5, 10, 0), # 4
                Point(7.5, 15, 0)]
    source_locs = [Point(-1,8,-15),#Order: MTAP
                    Point(3,12,-15),
                    Point(6,14,-15),
                    Point(7,9,-15)]
    signals = []
    source_locs_ordered = []
    for valve, source in zip (model.valves, source_locs):
        model.valves = [valve]
        t_model, heart_sound = model.generate_model(use_transfer=True)
        signals.append(heart_sound)
        source_locs_ordered.append(source)

    model = Model_3D(config, source_locs_ordered, mic_locs)
    model.generate(signals)
    
    config = ConfigParser()

    signals = model.signals
    plot(signals, model.Fs)