import numpy as np
from scipy.signal import ShortTimeFFT
from scipy.io import wavfile
from pathlib import Path
from typing import Literal
from lib.localization.LocalizationParams import LocalizationParams

    
def prepare(params: LocalizationParams, win: tuple, path: str|Path):
    # Fixed values for processing
    SFT = ShortTimeFFT.from_window(win, params.Fs, nperseg = 256 ,noverlap=128, scale_to='magnitude', phase_shift=None)
    
    signals = []
    for file in Path(path).glob("*_[0-6].wav"):
        rate,signal = wavfile.read(file)
        signals.append(signal)
        assert rate == params.Fs, f"Set rate {params.Fs} Hz does not match read rate {rate} Hz"
    
    assert len(signals) == 6, f"Expected 6 channels, got {len(signals)}"
    Sx_all=np.stack([SFT.stft(signal) for signal in signals])
    f_bins = SFT.f
    
    print(f"Sx_all has shape {Sx_all.shape}")

    f_bins = SFT.f

    delta_f = f_bins[1] - f_bins[0]
    print(f"Delta_f is {delta_f}")
    
    return Sx_all, delta_f
