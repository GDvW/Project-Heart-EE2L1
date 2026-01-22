import numpy as np
from scipy.io import wavfile
from matplotlib import pyplot as plt
import os

def load_recs(path):
    recordings = {}
    base_path = path
    for fname in os.listdir(path):

        if not fname.lower().endswith(".wav"):
            continue
        channel = int(fname[-5])
        path = os.path.join(base_path, fname)
        fs, x = wavfile.read(path)      
        recordings[channel] = x 

    channels = sorted(recordings.keys())

    num_channels = len(channels)
    #num_samples = min(len(recordings[ch]) for ch in channels)
    #too many samples
    num_samples = fs
    X = np.zeros((num_channels, num_samples))

    for i, ch in enumerate(channels):
        X[i, :] = recordings[ch][num_samples:2*num_samples]
    return X

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


def calibrate(recordings,reference,percentile=1):
    
    #reference: mean, median or channel
    #percentile: None for max-min, or 1 for example for P99-P1
    
    recordings = list(recordings)

    pp_values = np.array([
        peaktopeak(x, percentile=percentile) for x in recordings
    ])

    if isinstance(reference,str):
        if reference == 'mean':
            pp_ref = np.mean(pp_values)
        elif reference == 'median':
            pp_ref = np.median(pp_values)
    else: 
        pp_ref = peaktopeak(reference, percentile=percentile)  #channel data

   
    scales = pp_ref / pp_values

    calibrated = [
        recordings[i] * scales[i] for i in range(len(recordings))
    ]

    return calibrated, scales, pp_values


if __name__ == "__main__":
    


    #Run for first four channels [1,2,3,4] to calibrate with either mean or median as reference
    #Then run for the last four channels [3,4,5,6] with reference channel either 3 or 4 from the second experiment when the source is moved

    path_first = r'C:\Users\konst\Downloads\recordings\recordings\1234_300hz' #300 Mick
    path_second = r'C:\Users\konst\Downloads\recordings\recordings\3456_300hz'

    X1 = load_recs(path_first)
    X2 = load_recs(path_second)
    x1 = X1[0, :];   x2 = X1[1, :]; x3 = X1[2, :]; x4 = X1[3, :]; 
    x5 = X2[4, :];   x6 = X2[5,:]#x6 = np.zeros_like(x5)  
    recs1 = [x1,x2,x3,x4]
    recs2 = [x3,x4,x5,x6]
    calibrated_first_four, scales_first, pp = calibrate(
        recs1,
        reference='median',
        percentile=1
    )
    calibrated_second_four, scales_second, pp = calibrate(
        recs2,
        reference=calibrated_first_four[2],  #channel 3 as reference, could also be channel 4
        percentile=1
    )
    calibrated_all = calibrated_first_four[:2] + calibrated_second_four
    scales = np.concatenate([scales_first[:2], scales_second])
    print("Scaling factors:", scales)
    #scales = np.array([1.39298693,1.01174087,0.88995514,0.9885285,1.08169319,0.87358769])
    #scales = np.array([1.00994308, 0.74403375, 1.36581773, 0.99025079, 0.91486314, 0.95251508])
    plt.figure()
    for i in range(X1.shape[0]):
        plt.subplot(X1.shape[0],1,i+1)
        if i < 5:
            plt.plot(X1[i], label='Original')
        else:
            plt.plot(X2[i], label='Original')
        plt.plot(calibrated_all[i], label='Calibrated')
        plt.legend()
    plt.figure()
    for i in range(X1.shape[0]):
        plt.plot(calibrated_all[i], label=f'Calibrated channel {i+1}')
        plt.legend()
    plt.show()
    
#Test on Experiment 3
    #test_path = r'C:\Users\konst\Desktop\TU Delft\TA\3D local\experiment3sinemic1 1\home\ip3\audio_web_server\recordings'
    test_path = r'C:\Users\konst\Desktop\TU Delft\TA\3D local\recordings_20251013-151721(white silent)\home\ip3\audio_web_server\recordings'
    #test_path = r'C:\Users\konst\Downloads\Phantom\Phantom\PhantomS0'
    X_test = load_recs(test_path)
    X_test_calibrated = [X_test[i] * scales[i] for i in range(X_test.shape[0])]
    num_channels = X_test.shape[0]
    
    plt.figure()
    for i in range(num_channels):
        plt.subplot(num_channels,1,i+1)
        plt.plot(X_test[i], label='Original')
        plt.plot(X_test_calibrated[i], label='Calibrated')
        plt.legend()

    plt.figure()
    for i in range(num_channels):
        plt.plot(X_test_calibrated[i][20000:23000], label=f'Calibrated channel {i+1}')
        plt.legend()

    plt.figure()
    for i in range(num_channels):
        plt.plot(X_test[i][20000:23000], label=f'Original channel {i+1}')
        plt.legend()
    plt.show()
    

    #scales 100Hz[1.39298693 1.01174087 0.88995514 0.9885285  1.08169319 0.87358769]
    #scales 200Hz [1.00994308 0.74403375 1.36581773 0.99025079 0.91486314 0.95251508]
    #scales 300

