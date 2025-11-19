import matplotlib.pyplot as plt
from matplotlib import axes
from scipy.fft import fft, fftshift
import numpy as np

def getDamping(x: list|np.ndarray, freq:int, Fs: int, resolution: int|None = None):
    if resolution is not None:
        X = fft(x, resolution)
    else:
        X = fft(x)
    
    index = round(freq * len(X) / Fs)
    
    return (index * Fs / len(X), 1/X[index])