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
            "phantom_silent_t",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-152054(silent t)"),
            0.027,
            1,
            standard_mic_locations,
            np.array([hole_locations[0]])
        ),
        Sample(
            "phantom_silent_white",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-151542 (silent white)"),
            0.0145,
            1,
            standard_mic_locations,
            np.array([hole_locations[0]])
        ),
        Sample(
            "phantom_white_white",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-151829(white white)"),
            0.007,
            2,
            standard_mic_locations,
            hole_locations
        ),
        Sample(
            "phantom_white_silent",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-151721(white silent)"),
            0.01,
            1,
            standard_mic_locations,
            np.array([hole_locations[1]])
        ),
        Sample(
            "phantom_m_t",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-152153(m t)"),
            0.005,
            2,
            standard_mic_locations,
            hole_locations
        ),
        Sample(
            "phantom_m_silent",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.PhantomMap, "recordings_20251013-151945(m silent)"),
            0.005,
            1,
            standard_mic_locations,
            np.array([hole_locations[1]])
        )
    ],
    "Real":[
        Sample(
            "real_27cb1086-5d2c-4e5f-b29c-a8c6f9a40b84",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.RealMap, "27cb1086-5d2c-4e5f-b29c-a8c6f9a40b84"),
            0.02,
            2,
            standard_mic_locations,
            np.array([])
        ),
        Sample(
            "real_0a3adb22-9310-42db-80fc-3f085127cd6c",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.RealMap, "0a3adb22-9310-42db-80fc-3f085127cd6c"),
            0.015,
            2,
            standard_mic_locations,
            np.array([])
        ),
        Sample(
            "real_4ba65368-bc5a-4263-a66b-642c82aec8d1",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.RealMap, "4ba65368-bc5a-4263-a66b-642c82aec8d1"),
            0.015,
            2,
            standard_mic_locations,
            np.array([])
        ),
        Sample(
            "real_72f17780-170f-4a82-8962-9f80818bf4ac",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.RealMap, "72f17780-170f-4a82-8962-9f80818bf4ac"),
            0.015,
            2,
            standard_mic_locations,
            np.array([])
        ),
        Sample(
            "real_9489d50d-9398-4cfe-9c2f-0d0c9ee67536",
            Path(config.Recordings.SoundsPath).joinpath(config.Recordings.RealMap, "9489d50d-9398-4cfe-9c2f-0d0c9ee67536"),
            0.015,
            2,
            standard_mic_locations,
            np.array([])
        ),
    ]
}

GENERATED_MODEL_SAMPLES = {
    "S1": [
        Sample(
            "Generated_S1_sounds",
            "generated\\segmentation\\3D model heartsimulation\\without zeros\\raw\\S1",
            0.015,
            2,
            standard_mic_locations,
            np.array([
                (-0.020,0.021,-0.15),
                (0.005,-0.056,-0.15)
            ])
        )
    ],
    "S2": [
        Sample(
            "Generated_S2_sounds",
            "generated\\segmentation\\3D model heartsimulation\\without zeros\\raw\\S2",
            0.015,
            2,
            standard_mic_locations,
            np.array([
                (0.001,0.0025,-0.15),
                (0.025,-0.030,-0.15)
            ])
        )
    ]
}