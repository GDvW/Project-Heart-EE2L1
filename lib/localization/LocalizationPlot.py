import numpy as np
from scipy.signal.windows import gaussian
from pathlib import Path
import matplotlib.pyplot as plt
from copy import deepcopy
from lib.localization.LocalizationParams import LocalizationParams
from lib.localization.Localization import *
from src.localization_3D.loc import * 

class LocalizationPlot:
    def __init__(self, folder_path):
        self.root = Path(folder_path)
        
        self.params = LocalizationParams(
            bin = 4,
            z = 0.10,
            Fs = 48_000,
            Q = 2,
            M = 6,
            v_sound = 340,
            d = 0.10,
            resolution = 0.001,
            mode = "music"
        )
        
        self.source_locs = np.array([(0,0.025,0.15), (0,-0.025,0.15)] )
        
        self.old_params = deepcopy(self.params)
        
        self.x_range = [-0.08, 0.12]
        self.y_range = [-0.08, 0.12]
        
        self.win = ('gaussian', 256)
        self.fig = None
        self.image = None
        self.Pout = None
        self.Rx = None
        self.scan_points = None
        self.mic_positions = None
        self.f0 = None
        
        self.Sx_all, self.delta_f = prepare(self.params, self.win, self.root)
    
    def localize(self):
        assert self.params.mode in ["music", "mvdr"], "Mode should be either `music` or `mvdr`"

        if self.Rx is None or self.f0 is None or self.params.is_bin_updated(self.old_params):
            self.f0 = self.params.bin*self.delta_f
            print(f"Central frequency: {self.f0} Hz")
        
            X = self.Sx_all[:,self.params.bin,:]
            print(f"X has shape {X.shape}")

            self.Rx = (X @ X.conj().T) / X.shape[1]
            
        if self.params.is_scan_points_updated(self.old_params) or self.scan_points is None:
            self.scan_points = generate_scan_points(self.x_range, self.y_range, self.params.z, self.params.resolution)
        if self.mic_positions is None:
            self.mic_positions = generate_mic_positions()
        
        match self.params.mode:
            case "music":
                self.Pout = music_z(self.Rx, self.params.Q, self.params.M, self.scan_points, self.params.v_sound, self.f0, self.mic_positions)
            case "mvdr":
                self.Pout = mvdr_z(self.Rx, self.params.M, self.scan_points, self.params.v_sound, self.f0, self.mic_positions)
        
        self.old_params = deepcopy(self.params)
        
    def plot_init(self):
        self.localize()
        plt.ion()
        self.fig, ax = plt.subplots()
        
        self.image = ax.imshow(self.Pout[::-1], extent=(min(self.x_range), max(self.x_range), min(self.y_range), max(self.y_range)), cmap= "plasma")
        #self.image = ax.imshow(self.Pout[::-1]/np.max(self.Pout), extent=(min(self.x_range), max(self.x_range), min(self.y_range), max(self.y_range)), cmap= "plasma")
        ax.scatter(self.mic_positions[:,0], self.mic_positions[:,1], marker="x", color='white', label="Mic locs")
        ax.scatter(self.source_locs[:,0], self.source_locs[:,1], marker="v", color='white', label="Source loc")
        ax.legend()
    def plot_update(self):
        self.localize()
        
        self.image.set_data(self.Pout[::-1])#/np.max(self.Pout))
        self.fig.canvas.draw_idle()
    
    def print(self):
        print(self.params)
    def close(self):
        plt.close(self.fig)