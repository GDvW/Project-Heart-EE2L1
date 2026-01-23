from scipy.io import wavfile
from pathlib import Path
from os.path import join
import matplotlib.pyplot as plt
import numpy as np

from lib.config.ConfigParser import ConfigParser

config = ConfigParser()
root = Path(join(config.Recordings.SoundsPath, "recordings_20251013-152153(m t)"))

for i, file in enumerate(root.glob("*.wav")):
    Fs, sound = wavfile.read(file)
    t = np.linspace(0, Fs * len(sound), len(sound))
    plt.plot(t, sound, label=f"Mic {i}")
    
plt.legend()
plt.grid()
plt.show()
