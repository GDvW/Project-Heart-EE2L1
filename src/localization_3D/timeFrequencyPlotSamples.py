import matplotlib.pyplot as plt
from pathlib import Path
from scipy.io import wavfile
import os
from os.path import join
from time import sleep

from lib.samples.Samples import *
from lib.plot.timeFrequencyPlot import timeFrequencyPlot
# plt.ion()
if os.getenv("USE_LARGE_FONT") == "1":
    plt.rcParams.update({
        'font.size': 28,
        "lines.markersize": 16,
        "patch.edgecolor": "black", 
        "scatter.edgecolors": "black"
    })
    PLOTTING = True
else:
    PLOTTING = False

def saveTimeFreqPlots(sample: Sample, path: str|Path):
    for soundfile in sample.root.glob("*.wav"):
        print(f"Plotting {soundfile}...")
        rate,signal = wavfile.read(soundfile)
        fig, ax = plt.subplots(1, 2, figsize=(24,12), constrained_layout=True)
        timeFrequencyPlot(
            signal, 
            rate, 
            ax[0], 
            ax[1], 
            apply_fftshift=True, 
            time_title="Time domain of recording", 
            freq_title="Frequency domain of recording"
        )
        fig.savefig(join(path, f"{soundfile.parent.stem}.{soundfile.stem}.png"), dpi=300, bbox_inches="tight")
        # plt.show()
        # plt.waitforbuttonpress()
        plt.close(fig)
        plt.clf()
        
if __name__ == "__main__":
    sample = SAMPLES["Phantom"][0]
    # sample = SAMPLES["Generated"][1]
    # manager = plt.get_current_fig_manager()
    # manager.window.showMaximized()
    for sampleseries in SAMPLES.values():
        for sample in sampleseries:
            saveTimeFreqPlots(sample, "D:\\_temp\\EE2L1GraphsCanBeDeletedAfter01022026\\TimeFrequencyPlots")