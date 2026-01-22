from pathlib import Path

from lib.config.ConfigParser import ConfigParser
from Calibration.Calibrator import Calibrator
from lib.samples.Utils import get_recordings

class CalibrateAll:
    def __init__(self, config: ConfigParser):
        self.calibrator = Calibrator()
        
        self.source_dir = Path(config.Recordings.UncalibratedPath)
        self.target_dir = Path(config.Recordings.SoundsPath)
        
        self.calibrator.get_scales(
            config.Calibration.FirstCalibrationRecordingPath,
            config.Calibration.SecondCalibrationRecordingPath
        )
    def run(self, inspect: bool = False):
        for recordings in get_recordings(self.source_dir):
            print(f"Processing {recordings.relative_to(self.source_dir)}")
            target_dir = self.target_dir.joinpath(recordings.relative_to(self.source_dir))
            target_dir.mkdir(exist_ok=True, parents=True)
            self.calibrator.scale(recordings, target_dir)
            if inspect: self.calibrator.check_calibration()
            
if __name__ == "__main__":
    config = ConfigParser()
    c = CalibrateAll(config)
    c.run(inspect=False)