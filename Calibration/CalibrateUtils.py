from pathlib import Path
from scipy.io.wavfile import read, write
import numpy as np
from typing import Literal

def get_filenames_sorted(root: Path|str):
    return sorted(Path(root).glob("*.wav"),
                       key=lambda path: int(path.stem.rsplit("_", 1)[1]))
    
def load_recs(root: Path|str):
    root = Path(root)
    
    signals = []
    Fs = None
    for file in sorted(root.glob("*.wav"),
                       key=lambda path: int(path.stem.rsplit("_", 1)[1])):
        rate, signal = read(file)
        if Fs is None: Fs = rate
        assert rate == Fs, "Sample rates do not match"
        signals.append(signal)
    return Fs, np.column_stack(signals)
        
def load_recs_sample(root: Path|str, num_samples: int|None = None):
    Fs, signals = load_recs(root)
    
    num_samples = Fs if num_samples is None else num_samples
    
    return Fs, signals[num_samples:2*num_samples]

def peaktopeak(x, percentile=None):
    """
    Peak to peak amplitude calulation
    If percentile is None: use max-min
    If percentile is e.g. 1: use P(100-p) - P(p)
    """
    x = np.asarray(x)
    x = x - np.mean(x)  # remove DC 

    if percentile is None:
        return np.max(x) - np.min(x)
    else:
        low = np.percentile(x, percentile)
        high = np.percentile(x, 100 - percentile)
        return high - low
    
def peaktopeak_all(recordings, percentile=None):
    # recordings: shape (samples, channels)
    x = recordings - recordings.mean(axis=0, keepdims=True)

    if percentile is None:
        return x.max(axis=0) - x.min(axis=0)
    else:
        low = np.percentile(x, percentile, axis=0)
        high = np.percentile(x, 100 - percentile, axis=0)
        return high - low

def calibrate(recordings:np.ndarray, reference: Literal["mean", "median", "channel"], percentile:float|None=1):
    #percentile: None for max-min, or 1 for example for P99-P1

    pp_values = peaktopeak_all(recordings, percentile)

    if isinstance(reference, str):
        match reference:
            case 'mean':
                pp_ref = np.mean(pp_values)
            case 'median':
                pp_ref = np.median(pp_values)
    else:
        pp_ref = peaktopeak(reference, percentile=percentile)  #channel data

    scales = pp_ref / pp_values

    calibrated = recordings * scales
    return calibrated, scales, pp_values