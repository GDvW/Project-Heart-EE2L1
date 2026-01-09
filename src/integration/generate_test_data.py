import matplotlib.pyplot as plt
import numpy as np
from pathlib import Path
from os.path import join
from copy import deepcopy

from lib.model.Model import Model
from lib.config.ConfigParser import ConfigParser
from lib.general.generalUtils import white_noise, write_stereo

config = ConfigParser()
generated_path = Path(config.TestData.SoundsPath)
generated_path.mkdir(parents=True, exist_ok=True)

DURATION = config.TestData.Duration
Fs = config.TestData.Fs

# one source playing white noise
silent = np.zeros(DURATION*Fs)
white_noise_1 = white_noise(DURATION, Fs)
white_noise_2 = white_noise(DURATION, Fs)

write_stereo(silent, white_noise_1, Fs, join(generated_path, "Phantom", "Silent-White.wav"))
write_stereo(white_noise_1, silent, Fs, join(generated_path, "Phantom", "White-Silent.wav"))
write_stereo(white_noise_1, white_noise_2, Fs, join(generated_path, "Phantom", "White-White.wav"))

model = Model(config, randomize_enabled=False)
model.import_csv(".\\src\\module_2\\model_test_params.csv")
model.set_n(config.TestData.NBeats)

m_valve = [valve for valve in model.valves if valve.name=="M"][0]
t_valve = [valve for valve in model.valves if valve.name=="T"][0]

model.valves = [m_valve]
_, m_signal = model.generate_model(use_transfer=True)

model.valves = [t_valve]
_, t_signal = model.generate_model(use_transfer=True)

assert t_signal.shape == m_signal.shape
valve_silent = np.zeros(shape=t_signal.shape)

write_stereo(m_signal, valve_silent, Fs, join(generated_path, "Phantom", "M-Silent.wav"))
write_stereo(valve_silent, t_signal, Fs, join(generated_path, "Phantom", "Silent-T.wav"))
write_stereo(m_signal, t_signal, Fs, join(generated_path, "Phantom", "M-T.wav"))
#Normal
# model = Model(config, randomize_enabled=False)
# model.import_csv(".\\src\\module_2\\model_params.csv")
# model.set_n(config.TestData.NBeats)

# m_valve = [valve for valve in model.valves if valve.name=="M"][0]
# t_valve = [valve for valve in model.valves if valve.name=="T"][0]

# model.valves = [m_valve]
# _, m_signal = model.generate_model(use_transfer=True)

# model.valves = [t_valve]
# _, t_signal = model.generate_model(use_transfer=True)

# assert t_signal.shape == m_signal.shape
# valve_silent = np.zeros(shape=t_signal.shape)

# write_stereo(m_signal, valve_silent, Fs, join(generated_path, "Phantom", "M-Silent-NT.wav"))
# write_stereo(valve_silent, t_signal, Fs, join(generated_path, "Phantom", "Silent-T-NT.wav"))
# write_stereo(m_signal, t_signal, Fs, join(generated_path, "Phantom", "M-T-NT.wav"))
