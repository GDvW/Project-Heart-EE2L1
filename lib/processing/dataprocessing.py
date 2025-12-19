from scipy import signal
import numpy as np
from enum import Enum
from typing import Callable, Tuple
from scipy.signal import find_peaks

class HeartSound (Enum):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    S1 = 0
    S2 = 1

def get_peaks(x: np.ndarray, min_height: float, min_dist: float):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    peaks, properties = signal.find_peaks(x, height=min_height, distance=min_dist)

    return peaks, properties

def get_dist_peaks_to_next(x_peaks: np.ndarray):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    diff = np.diff(x_peaks)
    return dict(zip(x_peaks[:-1], diff))

def remove_outliers(x: list[tuple[int, int]]):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    x = np.array(x)
    dist = x[:,1]
    Q1 = np.percentile(dist, 25)
    Q3 = np.percentile(dist, 75)
    
    IQR = Q3 - Q1
    
    lower_bound = Q1 - 1.5 * IQR
    upper_bound = Q3 + 1.5 * IQR
    
    outliers = x[(dist < lower_bound) | (dist > upper_bound)]
    data = x[(dist >= lower_bound) & (dist <= upper_bound)]
    
    return data, outliers

def analyze_diff2(x_peaks: np.ndarray, diff: np.ndarray, diff2: np.ndarray):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    minima = []
    maxima = []
    uncertain = []
    previous_d = None
    for i, peak, d in zip(range(len(x_peaks)-1), x_peaks[:-1], [*diff2, None]):
        to_add = (peak, diff[i])
        if d is None and previous_d is None:
            if minima[-1] > maxima[-1]: maxima.append(to_add)
            else: minima.append(to_add)
        elif (d is None or d < 0) and (previous_d is None or previous_d > 0):
            maxima.append(to_add)
        elif (d is None or d >= 0) and (previous_d is None or previous_d <= 0):
            minima.append(to_add)
        else:
            uncertain.append(to_add)
        previous_d = d
            
    maxima, max_outliers = remove_outliers(maxima)
    minima, min_outliers = remove_outliers(minima)
    
    return maxima, max_outliers, minima, min_outliers

def classify_peaks(x_peaks: np.ndarray):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    raise NotImplementedError()
    diff = np.diff(x_peaks)
    diff2 = np.diff(diff)
    
    s2_peaks, s2_outliers, s1_peaks, s1_outliers = analyze_diff2(x_peaks, diff, diff2)
    
    return np.array(s1_peaks), np.array(s2_peaks), np.array(s1_outliers), np.array(s2_outliers)

def pop_np(x):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    return x[-1], x[:-1]

def get_difference(a,b):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    a_rows = {tuple(row) for row in a}
    b_rows = {tuple(row) for row in b}
    
    return list(a_rows - b_rows)

def detect_peak_domains(s1_peaks: np.ndarray, s2_peaks: np.ndarray, see: np.ndarray, threshold: float, verbose: bool = True):
    ind_s1 = detect_peak_domains_single_sound(s1_peaks, see, threshold)
    ind_s2 = detect_peak_domains_single_sound(s2_peaks, see, threshold)
    
    domains = np.r_[ind_s1, ind_s2]
    unique_domains, counts = np.unique(domains, axis=0, return_counts=True)
    if len(unique_domains) != len(domains):
        # There are overlapping segments, threshold should be increased
        # We suppose only a consquential S1 and S2 can overlap, not S2 and then S1, because the diastole is longer, but this was not true
        duplicates = unique_domains[counts > 1]
        duplicate_count = counts[counts > 1]
        for cur_domain, count in zip(duplicates, duplicate_count):
            s1_peak_in_domain = s1_peaks[(s1_peaks[:,0] >= cur_domain[0]) & (s1_peaks[:,0] <= cur_domain[1])]
            s2_peak_in_domain = s2_peaks[(s2_peaks[:,0] >= cur_domain[0]) & (s2_peaks[:,0] <= cur_domain[1])]
            if len(s1_peak_in_domain) + len(s2_peak_in_domain) != count:
                if verbose: print(f"WARNING [Segmentation]: Different amount of peaks in domain than count of domains ({len(s1_peak_in_domain) + len(s2_peak_in_domain)} != {count})")
                ind_s1 = ind_s1[np.all(ind_s1 != cur_domain, axis=1)]
                ind_s2 = ind_s2[np.all(ind_s2 != cur_domain, axis=1)]
                continue
            
            merged = [(s1[0], "S1") for s1 in s1_peak_in_domain] + [(s2[0], "S2") for s2 in s2_peak_in_domain]
            merged.sort(key=lambda x: x[0])
            
            pairs = [(merged[i][0], merged[i][1], merged[i+1][0]) for i in range(len(merged) - 1)]
            pairs.append((merged[-1][0], merged[-1][1], cur_domain[1]))
            
            new_domains = []
            previous_index = cur_domain[0]
            for first, first_type, second in pairs:
                inv_peaks, _ = find_peaks(-see[first:second+1])
                if len(inv_peaks) == 0:
                    print(f"ERROR: No minimums between {first} and {second}. Resulting data will be invalid")
                    continue
                inv_peaks_height = see[inv_peaks]
                
                split_index = inv_peaks[np.argmin(inv_peaks_height)] + first
                
                if split_index in [first, second]:
                    inv_peaks = inv_peaks[inv_peaks_height.argsort()] + first
                    for peak in inv_peaks:
                        if not split_index in [first, second]:
                            break
                    else: 
                        print(f"ERROR: No eligible minimums between {first} and {second}. Resulting data will be invalid")
                        
                
                new_domains.append([previous_index, split_index, first_type])
                previous_index = split_index
                
            ind_s1 = ind_s1[np.all(ind_s1 != cur_domain, axis=1)]
            ind_s2 = ind_s2[np.all(ind_s2 != cur_domain, axis=1)]
            
            for new_domain in new_domains:
                if new_domain[2] == "S1":
                    ind_s1 = np.r_[ind_s1, [new_domain[:2]]]
                elif new_domain[2] == "S2":
                    ind_s2 = np.r_[ind_s2, [new_domain[:2]]]
                else:
                    print(f"WARNING: invalid peak type: {new_domain[2]}")

    return ind_s1, ind_s2
def detect_peak_domains_single_sound(peaks: np.ndarray, see: np.ndarray, threshold: float): 
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    peak_start = None
    peaks_ind = []
    for i, s in enumerate(see):
        if s >= threshold and peak_start is None:
            peak_start = i
        elif s <= threshold and peak_start is not None:
            if np.any((peaks[:,0] >= peak_start) & (peaks[:,0] <= i)):
                peaks_ind.append((peak_start, i))
            peak_start = None
            
    return np.array(peaks_ind)

def segment_only_with_len_filter_and_thus_deprecated_should_not_be_used(signal: np.ndarray, domains: np.ndarray, len_filter: int):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    mask = np.zeros(len(signal), dtype=bool)
    comp = int(len_filter / 2)
    for start, end in domains:
        mask[start - comp:end - comp] = True
    return np.where(mask, signal, 0)

def segment(signal: np.ndarray, domains: np.ndarray, comp: Callable[[int], int]) -> Tuple[np.ndarray, np.ndarray]:
    """
    @author: Gerrald
    @date: 10-12-2025
    
    _summary_

    Args:
        signal (np.ndarray): The signal to segment
        domains (np.ndarray): The domains to segment on.
        comp (Callable[[int], int]): A compensation function that relates the indices of the domains to the indices of the input signal

    Returns:
        Tuple[np.ndarray, np.ndarray]: A segmented signal that leaves zero outside the domains, and a signal that removes those `silent` parts.
    """
    mask = np.zeros(len(signal), dtype=bool)
    concatenated = []
    for start, end in domains:
        mask[comp(start):comp(end)] = True
        concatenated.extend(signal[comp(start):comp(end)])
    return np.where(mask, signal, 0), np.array(concatenated) 