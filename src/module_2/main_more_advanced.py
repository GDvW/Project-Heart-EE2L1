from scipy.signal import TransferFunction, impulse, zpk2tf
import numpy as np
import matplotlib.pyplot as plt
from lib.config.ConfigParser import ConfigParser
import sounddevice as sd
from lib.processing.functions import construct_bandpass_filter, apply_filter
from os.path import join
from scipy.io.wavfile import write

class ValveParams:
    def __init__(self, duration_ms: float, freq: float, ampl:float, delay_ms:float, onset_ms:float, name: str=None):
        self.duration = duration_ms / 1000
        self.freq = freq
        self.ampl = ampl
        self.delay = delay_ms / 1000
        self.onset = onset_ms / 1000
        self.name = name

def advanced_model_valve_params(params: ValveParams, Fs:int):
    return advanced_model_valve(params.duration, params.freq, params.ampl, params.delay, params.onset, Fs)

def advanced_model_valve(duration: float, freq:float, ampl:float, delay:float, onset:float, Fs:int):
    a = 10
    onset_ampl = 0.1
    omega = 2*np.pi*freq
    
    # Create the transfer function system of the sound
    b, a = zpk2tf([], [a-1j*omega, a+1j*omega], omega)
    system = TransferFunction(b, a)
    # Time array (from 0 to duration with step size of 1/Fs)
    t = np.linspace(0, onset, int(Fs * onset))
    # Impulse response (time domain)
    t_onset, h_onset = impulse(system, T=t)
    
    a = 1/duration
    omega = 2*np.pi*freq
    # Create the transfer function system of the sound
    b, a = zpk2tf([], [-a-1j*omega, -a+1j*omega], omega)
    system = TransferFunction(b, a)
    # Time array (from 0 to duration with step size of 1/Fs)
    t = np.linspace(0, duration, int(Fs * duration))
    # Impulse response (time domain)
    t_beat, h_beat = impulse(system, T=t)
    
    
    # Assemble reponse
    samples_delay = int(Fs * delay)
    h_out = ampl*np.concatenate([np.zeros(samples_delay), onset_ampl*h_onset, h_beat])
    t_out = np.linspace(0, delay+duration+onset, len(h_out))
    
    return t_out, h_out

def advanced_model():
    config = ConfigParser()
    valves = [
        ValveParams(20,  50,   1,  10, 10, "M"),
        ValveParams(20, 150, 0.5,  40, 10, "T"),
        ValveParams(20,  50, 0.5, 300, 10, "A"),
        ValveParams(20,  30, 0.4, 330, 10, "P"),
    ]
    Fs = config.HeartSoundModel.Fs
    BPM = config.HeartSoundModel.BPM
    n = config.HeartSoundModel.NBeats
    t_out = []
    h_out = []
    for valve in valves:
        t, h = advanced_model_valve_params(valve, Fs)
        t_out.append(t)
        h_out.append(h)
    
    h_len = int(60/BPM*Fs)
    
    t_total = np.linspace(0, 60/BPM, h_len)
    h_total = np.zeros(h_len)
    for h in h_out:
        if len(h) <= h_len:
            h = np.pad(h, (0, h_len - len(h)))
            h_total += h
        else:
            raise RuntimeError("One beat longer than reserved space")
    
    g = construct_bandpass_filter(
        config.LowpassFilter.LowFrequency,
        config.LowpassFilter.HighFrequency,
        Fs,
        order=config.LowpassFilter.FilterOrder,
        size=config.LowpassFilter.Size
    )
    h_filtered = apply_filter(h_total, g)
    t_filtered = np.linspace(-len(g), len(h_filtered)/Fs, len(h_filtered))
    
    h_sth = np.tile(h_total, n)
    t_sth = np.linspace(0, len(h_sth)/Fs, len(h_sth))
    h_tot_filt = apply_filter(h_sth, g)
    t_tot_filt = np.linspace(-len(g)/(2*Fs), len(h_sth)/Fs+len(g)/(2*Fs), len(h_tot_filt))
    write(join(config.Generation.SoundsPath, f"Advanced-{Fs}Hz-{BPM}BPM-{n} beats.wav"), Fs, h_tot_filt)
    sd.play(h_tot_filt, Fs)
    
    plt.plot(t_sth, h_sth, label="original")
    plt.plot(t_tot_filt, h_tot_filt, label="filtered")
    plt.title("Advanced")
    plt.legend()
    plt.grid()
    plt.show()

if __name__ == "__main__":
    advanced_model()
