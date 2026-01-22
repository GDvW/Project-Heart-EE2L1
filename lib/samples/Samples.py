from dataclasses import dataclass
from typing import Literal, Tuple
from pathlib import Path
import numpy as np

from lib.config.ConfigParser import ConfigParser
# Library to work with samples
@dataclass
class Sample:
    name: str
    root: Path
    z: float
    n_sources: int
    mic_locs: np.ndarray[Tuple[float,float,float]]
    source_locs: np.ndarray[Tuple[float,float,float]]
    
standard_mic_locations = np.array([
    (-0.025, 0.05, 0),  # 0
    ( 0.025, 0.05, 0),  # 1
    (-0.025, 0,    0),  # 2
    ( 0.025, 0,    0),  # 3
    (-0.025, -0.05, 0), # 4
    ( 0.025, -0.05, 0)  # 5
])

hole_locations = np.array([
    (0,-0.025,0.15),
    (0,0.025,0.15)
])

config = ConfigParser()
    
SAMPLES_CALIBRATED = {
    "Phantom": [
        Sample(
            "Calibrated_MT",
            Path("samples\\calibrated_MT"),
            0.02,
            2,
            standard_mic_locations,
            hole_locations
        ),
        Sample(
            "Calibrated_White_Noise_Single",
            Path("samples\\calibrated_white_noise_single"),
            0.02,
            1,
            standard_mic_locations,
            np.array([hole_locations[1]])
        )
    ],
    "Generated": [
        Sample(
            "White_Noise_Single",
            Path("generated\\hearbeat model\\3d-model\\White_Noise_Single"),
            0.015,
            1, 
            standard_mic_locations,
            np.array([hole_locations[1]])
        ),
        Sample(
            "White_Noise_Double",
            Path("generated\\hearbeat model\\3d-model\\White_Noise_Double"),
            0.015,
            2,
            standard_mic_locations,
            hole_locations
        )
    ]
}

SAMPLES_SELF_CALIBRATED = {
    "Phantom":[
        Sample(
            "Silent_White",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-151542 (silent white)"),
            0.015,
            1,
            standard_mic_locations,
            np.array([hole_locations[1]])
        )
    ],
    "Real":[
        
    ]
}