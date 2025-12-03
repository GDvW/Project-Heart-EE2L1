from scipy.signal import TransferFunction, impulse, zpk2tf
import numpy as np
import matplotlib.pyplot as plt
from lib.config.ConfigParser import ConfigParser
import sounddevice as sd
from lib.processing.Processor import Processor
from lib.processing.functions import construct_bandpass_filter, apply_filter
from os.path import join
from scipy.io.wavfile import write
from src.module_2.generate import *

from matplotlib.widgets import Button, Slider
def getData():
    config = ConfigParser()

    t_model, h_model = advanced_model(config) 
    
    return t_model, h_model

def timeOriginal(shift, length, Fs):
    return np.linspace(shift, shift+length/Fs, length)
    
def matchParams():
    config = ConfigParser()
    Fs = config.HeartSoundModel.Fs
    BPM = config.HeartSoundModel.BPM
    n = config.HeartSoundModel.NBeats
    len_g = config.LowpassFilter.Size
    lf = config.LowpassFilter.LowFrequency
    hf = config.LowpassFilter.HighFrequency
    order=config.LowpassFilter.FilterOrder
    size=config.LowpassFilter.Size
    
    # Define params
    valves = [
        ValveParams(20,  50,   1,  10, 10, "M"),
        ValveParams(20, 150, 0.5,  40, 10, "T"),
        ValveParams(20,  50, 0.5, 300, 10, "A"),
        ValveParams(20,  30, 0.4, 330, 10, "P"),
    ]
    
    # Get original heart sound
    processor = Processor("samples\\stethoscope_2_realHeart_\\recording_2025-07-10_14-34-04_channel_1.wav", config, save_steps=True, write_result_processed=False, write_result_raw=False)
    processor.process()
    
    init_shift = -2.28
    t_model, h_model = advanced_model(
        Fs,
        BPM,
        lf,
        hf,
        order,
        size,
        valves
    ) 
    
    fig, ax = plt.subplots()    
    
    modelplot, = ax.plot(t_model, h_model, label="Model")
    original, = ax.plot(timeOriginal(init_shift, len(processor.y_normalized), processor.Fs_target), processor.y_normalized, label="Real data")
    ax.set_xlim(min(t_model)-0.1, max(t_model)+0.1)
    ax.set_title("Advanced")
    ax.legend()
    ax.grid(True)
    
    fig.subplots_adjust(left=0.25, bottom=0.25)
    
    # Make a horizontal slider to control the frequency.
    axshift = fig.add_axes([0.25, 0.1, 0.65, 0.03])
    shift_slider = Slider(
        ax=axshift,
        label='Time (s)',
        valmin=-2.30,
        valmax=-2.25,
        valinit=init_shift,
    )
    def updateOriginal():
        original.set_xdata(timeOriginal(shift_slider.val, len(processor.y_normalized), processor.Fs_target))
        fig.canvas.draw_idle()
        
    def updateModel():
        valvesAdj = [
            ValveParams(20,  50,   1, slider4.val, 10, "M"),
            ValveParams(20, 150, 0.5, slider3.val, 10, "T"),
            ValveParams(20,  50, 0.5, slider2.val, 10, "A"),
            ValveParams(20,  30, 0.4, slider1.val, 10, "P"),
        ]
        _, h_model = advanced_model(
            Fs,
            BPM,
            lf,
            hf,
            order,
            size,
            valvesAdj
        ) 
        modelplot.set_ydata(h_model)
        fig.canvas.draw_idle()
        
        
    # Make a vertically oriented slider to control the amplitude
    axbpm1 = fig.add_axes([0.1, 0.25, 0.0225, 0.63])
    slider1 = Slider(
        ax=axbpm1,
        label="P",
        valmin=200,
        valmax=430,
        valinit=330,
        orientation="vertical"
    )
    axbpm2 = fig.add_axes([0.075, 0.25, 0.0225, 0.63])
    slider2 = Slider(
        ax=axbpm2,
        label="A",
        valmin=200,
        valmax=400,
        valinit=300,
        orientation="vertical"
    )
    axbpm3 = fig.add_axes([0.05, 0.25, 0.0225, 0.63])
    slider3 = Slider(
        ax=axbpm3,
        label="T",
        valmin=20,
        valmax=100,
        valinit=40,
        orientation="vertical"
    )
    axbpm4 = fig.add_axes([0.025, 0.25, 0.0225, 0.63])
    slider4 = Slider(
        ax=axbpm4,
        label="M",
        valmin=5,
        valmax=30,
        valinit=10,
        orientation="vertical"
    )
    resetax = fig.add_axes([0.8, 0.025, 0.1, 0.04])
    buttonOriginal = Button(resetax, 'Apply original', hovercolor='0.975')
    resetax = fig.add_axes([0.65, 0.025, 0.1, 0.04])
    buttonModel = Button(resetax, 'Apply model', hovercolor='0.975')


    def applyOriginal(event):
        updateOriginal()
    buttonOriginal.on_clicked(applyOriginal)
    def applyModel(event):
        updateModel()
    buttonModel.on_clicked(applyModel)
    
    plt.show()



if __name__ == "__main__":
    matchParams()