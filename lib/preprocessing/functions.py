from scipy import signal
import numpy as np
from math import floor

def construct_filter(low: float, high: float, Fs: int, order: int = 2, size: int = 2000):
    """Construct a bandpass non-causal Butterworth filter with a phase of 0.

    Args:
        low (float): The lower cutoff frequency in Hz.
        high (float): The higher cutoff frequency in Hz.
        Fs (int): The sampling frequency in Hz.
        order (int, optional): Half the order of the filter. Defaults to 2.
        size (int, optional): The length of the filter minus 1. Defaults to 2000.

    Returns:
        g (np.ndarray): returns the filter with length of size+1.
    """
    resolution = floor(size/2)
    
    b, a = signal.butter(order, [2*low/Fs, 2*high/Fs], btype="band")
    g = signal.filtfilt(b, a, [*np.zeros(resolution), 1, *np.zeros(resolution)])
    return g

def filter(x: list|np.ndarray, g: list|np.ndarray):
    """Filter x through g by convolution.

    Args:
        x (list | np.ndarray): The signal.
        g (list | np.ndarray): The filter.

    Returns:
        y (np.ndarray): The result.
    """
    return np.convolve(x, g)

def downsample(x: list|np.ndarray, Fs_original:int, Fs_target: int):
    """Downsample x from Fs_original Hz to Fs_target Hz. Only possible if Fs_original is a multiple of Fs_target.

    Args:
        x (list | np.ndarray): The signal to downsample.
        Fs_original (int): The original sampling frequency (Hz).
        Fs_target (int): The sampling frequency to convert to (Hz).

    Raises:
        ValueError: If Fs_original is not a multiple of Fs_target.

    Returns:
        x_downsampled (list | np.ndarray): The downsampled signal.
    """
    M = Fs_original / Fs_target
    
    if int(M) != M:
        print(f"ERROR: M is not an integer: {Fs_original}/{Fs_target}={M:.5f}")
        raise ValueError(f"ERROR: M is not an integer: {Fs_original}/{Fs_target}={M:.5f}")
    
    M = int(M)
    x_downsampled = x[::M]
    
    return x_downsampled
