import matplotlib.pyplot as plt
from pathlib import Path
from scipy.io import wavfile
import os
from os.path import join
from time import sleep
import gc

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

def saveTimeFreqPlots(sample: Sample, path: str|Path, just_a_sample: bool):
    for soundfile in sample.root.glob("*.wav"):
        print(f"Plotting {soundfile}...")
        rate,signal = wavfile.read(soundfile)
        if just_a_sample and len(signal) >= 3*rate: signal = signal[rate:3*rate]
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
        fig.savefig(join(path, f"{soundfile.parent.parent.stem}.{soundfile.parent.stem}.{soundfile.stem}.png"), dpi=300, bbox_inches="tight")
        # plt.show()
        # plt.waitforbuttonpress()
        plt.close(fig)
    gc.collect()
        
if __name__ == "__main__":
    sample = SAMPLES_CALIBRATED["Phantom"][0]
    # sample = SAMPLES_CALIBRATED["Generated"][1]
    # manager = plt.get_current_fig_manager()
    # manager.window.showMaximized()
    skipping = True
    for sampleseries in SAMPLES_CALIBRATED.values():
    # for sampleseries in SAMPLES_SELF_CALIBRATED.values():
        for sample in sampleseries:
            if "generated\\hearbeat model\\3d-model\\White_Noise_Single" == str(sample.root):
                skipping = False
            if skipping:
                continue
            saveTimeFreqPlots(sample, "D:\\_temp\\EE2L1GraphsCanBeDeletedAfter01022026\\TimeFrequencyPlotsSample", just_a_sample=True)