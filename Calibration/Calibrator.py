from pathlib import Path
from scipy.io.wavfile import read, write
import numpy as np
import matplotlib.pyplot as plt
from lib.config.ConfigParser import ConfigParser

from Calibration.CalibrateUtils import *

class Calibrator:
    def __init__(self):
        self.scales = None
        self.calibrated_all_ref = None
        self.original_ref = None
        self.last_calibrated = None
        self.last_original = None
        self.Fs = None
        
    def get_scales(self, first_calibration_dir:str|Path, second_calibration_dir:str|Path):
        Fs1, X1 = load_recs_sample(first_calibration_dir)
        Fs2, X2 = load_recs_sample(second_calibration_dir)
        assert Fs1 == Fs2, "Sample rates for 1st and 2nd recordings do not match"
        self.Fs = Fs1
        assert X1.shape[1] == 6, f"{first_calibration_dir} should contain 6 wav files, but has {X1.shape[1]}"
        assert X2.shape[1] == 6, f"{second_calibration_dir} should contain 6 wav files, but has {X2.shape[1]}"
        # Calibrate microphones 1-4
        recs1 = X1[:,:4]
        recs2 = np.c_[X1[:,2:4], X2[:,4:6]]
        calibrated_first_four, scales_first, _ = calibrate(
            recs1,
            reference="median",
            percentile=1
        )
        calibrated_second_four, scales_second, _ = calibrate(
            recs2,
            reference=calibrated_first_four[:,3],# 2 is 3rd, 3 (4th) could also be an option
            percentile = 1
        )
        
        self.scales = np.r_[scales_first[:2], scales_second]
        self.calibrated_all_ref = np.c_[calibrated_first_four[:,:2], calibrated_second_four]
        self.original_ref = np.c_[X1[:,:2], X2[:,2:]]

        print(f"Scaling factors: {self.scales}")
    def scale(self, unscaled_path: str|Path, output_path: str|Path|None):
        self.Fs, signals = load_recs(unscaled_path)
        
        calibrated = signals * self.scales
        
        self.last_original = signals
        self.last_calibrated = calibrated
        
        if output_path is None: return
        
        for filename, channel in zip(get_filenames_sorted(unscaled_path), calibrated.T):
            write(Path(output_path).joinpath(f"{filename.stem}.wav"), self.Fs, channel)
        
    def check_calibration(self, reference: bool = False):
        """Generates plots to check whether calibration went succesfully.

        Args:
            reference (bool, optional): Whether to check the reference signals that made up the scaling factors. In case of False, uses the signals that were created. Defaults to False.
        """
        original = self.original_ref if reference else self.last_original[self.Fs:2*self.Fs]
        calibrated = self.calibrated_all_ref if reference else self.last_calibrated[self.Fs:2*self.Fs]
        
        if original is None or calibrated is None: return
        
        fig, axs = plt.subplots(self.original_ref.shape[1], 1, sharex=True, constrained_layout=True)
        for i, (ax, original_signal, calibrated_signal) in enumerate(zip(axs, original.T, calibrated.T)):
            t = np.linspace(0, self.Fs, len(original_signal))
            ax.set_title(f"Microphone {i+1}")
            ax.plot(t, original_signal, label=f'Original')
            ax.plot(t, calibrated_signal, label=f'Calibrated mic')
            ax.legend()
        plt.xlabel("t [s]")
        plt.ylabel("Amplitude [rel]")
        plt.figure()
        for i, calibrated_signal in enumerate(calibrated.T):
            t = np.linspace(0, self.Fs, len(calibrated_signal))
            plt.plot(t, calibrated_signal, label=f'Calibrated channel {i+1}')
        plt.xlabel("t [s]")
        plt.ylabel("Amplitude [rel]")
        plt.legend()
        plt.show()
        
    
if __name__ == "__main__":
    config = ConfigParser()
    calib = Calibrator()
    calib.get_scales(config.Calibration.FirstCalibrationRecordingPath, config.Calibration.SecondCalibrationRecordingPath)
    calib.check_calibration(True)