import numpy as np
from matched_beamformer import matchedbeamforming
from MVDR import MVDR
from scipy.signal import ShortTimeFFT
from scipy.signal.windows import gaussian
from scipy.io import wavfile
from pathlib import Path
import matplotlib.pyplot as plt


if __name__ == "__main__":
    fs = 48000
    win = ('gaussian', 1e-2 * fs)
    SFT = ShortTimeFFT.from_window(win, fs, nperseg = 256 ,noverlap=0, scale_to='magnitude', phase_shift=None)
    filepath1 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_1.wav")
    filepath2 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_2.wav")
    filepath3 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_3.wav")
    filepath4 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_4.wav")
    filepath5 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_5.wav")
    filepath6 = Path(r"C:\Users\kkouk\IP3\Project-Heart-EE2L1\samples\Linear array sample recordings\LinearArray-0-degrees\recording_2024-09-30_12-48-30_channel_6.wav")
    rate, signal1 = wavfile.read(filepath1)
    rate, signal2 = wavfile.read(filepath2)
    rate, signal3 = wavfile.read(filepath3)
    rate, signal4 = wavfile.read(filepath4)
    rate, signal5 = wavfile.read(filepath5)
    rate, signal6 = wavfile.read(filepath6)

    print(signal1.shape)
    
    Sx1 = SFT.stft(signal1)
    Sx2 = SFT.stft(signal2)
    Sx3 = SFT.stft(signal3)
    Sx4 = SFT.stft(signal4)
    Sx5 = SFT.stft(signal5)
    Sx6 = SFT.stft(signal6)

    Sx_all=np.stack((Sx1,Sx2,Sx3,Sx4,Sx5,Sx6))
    #print (Sx1.shape)
    print(Sx_all.shape)
    f_bins = SFT.f
    print(f_bins[1] - f_bins[0])
    X = Sx_all[:, 8, :]
    print(X.shape) 
    Rx = np.cov(X)

    M = 6
    d = 0.1
    v = 343
    f0 = f_bins[8]
    theta_range = np.array([i for i in range (-90,90)])
    pspec = MVDR(theta_range, M, d, v, f0, Rx)
    print ("done with MVDR")
    plt.figure()
    plt.plot(theta_range,pspec)
    plt.show()





