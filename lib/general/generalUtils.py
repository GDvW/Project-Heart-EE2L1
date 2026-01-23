import numpy as np
from random import random
from scipy.io.wavfile import write
from pathlib import Path

def todB(value: float|list|np.ndarray, power: bool = False) -> float | list | np.ndarray:
    """
    @author: Gerrald
    @date: 10-12-2025

    Convert a value from linear to dB.

    Args:
        value (float | list | np.ndarray): The value(s) to convert.
        power (bool, optional): Whether the value is a power value. If true, the result is 10 * log10(value), else 20 * log10(value). Defaults to False.

    Returns:
        float | list | np.ndarray: The dB values of the input.
    
    """
    return 10 * np.log10(value) * (1 if power else 2)
    
def fromdB(dB: float|list|np.ndarray, power: bool = False) -> float | list | np.ndarray:
    """
    @author: Gerrald
    @date: 10-12-2025

    Convert a value from dB to linear.

    Args:
        dB (float | list | np.ndarray): The dB value(s) to convert.
        power (bool, optional): Whether the value is a power value. If true, the result is 10 ^ (dB/10), else 10 ^ (dB/20). Defaults to False.

    Returns:
        float | list | np.ndarray: The linear values of the input.
    
    """
    return 10 ** (dB / (10 if power else 20))

def randomize(val: float, ratio: float) -> float:
    """
    @author: Gerrald
    @date: 10-12-2025
    
    Randomize a value.

    Args:
        val (float): The value to randomize
        ratio (float): The max random component in ratio of the value.

    Returns:
        float: The randomized value.
    """
    return val * (1 + ratio * random() * np.sign(random() - 0.5))

def white_noise(duration: float, Fs: int):
    """
    @author: Gerrald
    @date: 17-12-2025
    """
    return np.random.rand(round(duration * Fs)) * np.sign(np.random.rand(round(duration * Fs)) - 0.5)

def write_stereo(left: np.ndarray, right: np.ndarray, Fs: int, path: str, float_to_int_conversion: bool = False):
    """
    @author: Gerrald
    @date: 09-01-2026
    """
    Path(path).parent.mkdir(exist_ok=True, parents=True)
    assert left.shape == right.shape
    stereo = np.column_stack((left, right))
    if stereo.dtype in [np.float64, np.float32] and float_to_int_conversion:
        stereo = np.int16(stereo * 32767)
    write(path, Fs, stereo)
    
def get_unique_domains(domains: list[np.ndarray]):
    """
    @author: Gerrald
    @date: 14-01-2026
    """
    stacked_domains = np.stack(domains)

    full_domains = np.column_stack([ 
        stacked_domains[:,:,0].min(axis=0), # min of first column 
        stacked_domains[:,:,1].max(axis=0) # max of second column 
    ])

    return full_domains