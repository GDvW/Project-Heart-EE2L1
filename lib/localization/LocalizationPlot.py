import numpy as np
from scipy.signal.windows import gaussian
from pathlib import Path
import matplotlib.pyplot as plt
from copy import deepcopy
import os
from os.path import join
from lib.localization.LocalizationParams import LocalizationParams
from lib.localization.Localization import *
from src.localization_3D.loc import * 
from lib.localization.Utils import * 
from lib.samples.Samples import Sample

if os.getenv("USE_LARGE_FONT") == "1":
    plt.rcParams.update({
        'font.size': 30,
        "lines.markersize": 16,
        "patch.edgecolor": "black", 
        "scatter.edgecolors": "black"
    })
    linewidth = 5
    PLOTTING = True
else:
    PLOTTING = False
    linewidth = 2

class LocalizationPlot:
    def __init__(self, sample: Sample):
        self.root = Path(sample.root)
        self.sample_name = sample.name
        self.params = LocalizationParams(
            bin = 0,
            z = sample.z,
            Fs = 48_000,
            Q = sample.n_sources,
            M = 6,
            v_sound = 340,
            d = 0.10,
            resolution = 0.001,
            mode = "music"
        )
        
        self.source_locs = sample.source_locs
        
        self.old_params = deepcopy(self.params)
        
        self.x_range = [-0.08, 0.08]
        self.y_range = [-0.12, 0.12]
        # self.x_range = [-0.05, 0.05]
        # self.y_range = [-0.075, 0.075]
        
        self.win = ('gaussian', 256)
        self.fig = None
        self.image = None
        self.Pout = None
        self.Rx = None
        self.scan_points = None
        self.mic_positions = sample.mic_locs
        self.f0 = None
        self.likely_scatter = None
        
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
        
        match self.params.mode:
            case "music":
                self.Pout = music_z(self.Rx, self.params.Q, self.params.M, self.scan_points, self.params.v_sound, self.f0, self.mic_positions)
            case "mvdr":
                self.Pout = mvdr_z(self.Rx, self.params.M, self.scan_points, self.params.v_sound, self.f0, self.mic_positions)
                
        self.likely_source_locs = np.array([
            convert_coords_to_m(
                self.Pout,
                coord,
                self.x_range,
                self.y_range
            )
            for coord in top_n_coords(scale(self.Pout), self.params.Q)
            # for coord in top_n_coords(scale(self.Pout[::-1]), self.params.Q)
        ])
        
        self.old_params = deepcopy(self.params)
        
    def plot_init(self):
        self.localize()
        plt.ion()
        self.fig, ax = plt.subplots()
        
        sources = "source" if self.params.Q == 1 else "sources"
        
        self.image = ax.imshow(scale(self.Pout[::-1]), extent=(min(self.x_range), max(self.x_range), min(self.y_range), max(self.y_range)), cmap= "plasma")
        
        cbar = self.fig.colorbar(self.image)
        cbar.set_label("Normalized amplitude [dB]")
        #self.image = ax.imshow(self.Pout[::-1]/np.max(self.Pout), extent=(min(self.x_range), max(self.x_range), min(self.y_range), max(self.y_range)), cmap= "plasma")
        ax.scatter(self.mic_positions[:,0], self.mic_positions[:,1], marker="o", color='red', label="Microphones")
        ax.scatter(self.source_locs[:,0], self.source_locs[:,1], marker="+", color='black', label=f"True {sources}", linewidths=linewidth)
        self.likely_scatter = ax.scatter(self.likely_source_locs[:,0], self.likely_source_locs[:,1], marker="x", color='white', label=f"Estimated {sources}", linewidths=linewidth)
        ax.set_xlabel("x [m]")
        ax.set_ylabel("y [m]")
        if PLOTTING:
            ax.legend(fontsize=20)
        else:
            ax.legend()
    def plot_update(self):
        self.localize()
        
        self.image.set_data(scale(self.Pout[::-1]))#/np.max(self.Pout))
        self.likely_scatter.set_offsets(self.likely_source_locs)
        self.fig.canvas.draw_idle()
    
    def print(self):
        print(self.params)
    def close(self):
        plt.close(self.fig)
    def save(self, path):
        self.fig.savefig(path, dpi=300, bbox_inches="tight")
    def save_path(self, path):
        self.fig.savefig(join(path, f"{self.sample_name}---{self.params.to_filename(prefix="", ext='png')}"), dpi=300, bbox_inches="tight")