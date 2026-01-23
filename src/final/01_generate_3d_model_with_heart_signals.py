import numpy as np
import matplotlib.pyplot as plt
from lib.model.Model_3D import Model_3D, Point
from lib.general.generalUtils import white_noise
from lib.config.ConfigParser import ConfigParser
from lib.model.Model import Model


def apply_heart_model():
    config = ConfigParser()
    Fs = config.HeartSoundModel.Fs
    
    model = Model(config, randomize_enabled=False, simulate_S2=True)
    model.import_csv(".\\src\\module_2\\model_params.csv")
    model.set_n(100)
    mic_locs = [
        Point(-0.025, 0.05, 0),  # 0
        Point( 0.025, 0.05, 0),  # 1
        Point(-0.025, 0,    0),  # 2
        Point( 0.025, 0,    0),  # 3
        Point(-0.025, -0.05, 0), # 4
        Point( 0.025, -0.05, 0)  # 5
    ]
    source_locs = [Point(-0.020,0.021,-0.15),#Order: MTAP
                  Point(0.005,-0.056,-0.15),
                  Point(0.001,0.0025,-0.15),
                  Point(0.025,-0.030,-0.15)
    ]
    signals = []
    for valve, source in zip (model.valves, source_locs):
        model.valves = [valve]
        t_model, heart_sound = model.generate_model()
        signals.append(heart_sound)
    
    model = Model_3D(config, source_locs, mic_locs)
    
    h = model.generate(signals)
    model.save("HeartSimulation")
    
    return h
    

if __name__ == "__main__":
    h = apply_heart_model()
    # for i, x in enumerate(h):
    #     plt.plot(x, label=f"Mic {i}")
    # plt.legend()
    # plt.show()