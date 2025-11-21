from scipy import signal
import numpy as np
from enum import Enum

class HeartSound (Enum):
    S1 = 0
    S2 = 1

def get_peaks(x: np.ndarray, min_height: float, min_dist: float):
    peaks, properties = signal.find_peaks(x, height=min_height, distance=min_dist)

    return peaks, properties

def get_dist_peaks_to_next(x_peaks: np.ndarray):
    diff = np.diff(x_peaks)
    return dict(zip(x_peaks[:-1], diff))

def classify_peaks(x_peaks: np.ndarray):
    diff = np.diff(x_peaks)
    diff2 = np.diff(diff)
    
    s1_peaks = []
    s2_peaks = []
    for peak, d in zip(x_peaks[:-2], diff2):
        if d < 0:
            s2_peaks.append(peak)
        else:
            s1_peaks.append(peak)
    return np.array(s1_peaks), np.array(s2_peaks)