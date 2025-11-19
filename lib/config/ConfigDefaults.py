from pathlib import Path

CONFIG_PATH = Path.cwd() / "config.ini"

DEFAULT_CONFIG = {
    "LowpassFilter": {
        "FilterOrder": 3,
        "LowFrequency": 10,
        "HighFrequency": 800,
        "Size": 5000
    },
    "Downsampling":{
        "FsTarget": 4000
    }
}

DEFAULT_COMMENTS = {
    "LowpassFilter": ["# Properties of the lowpass filter"],
    "Downsampling": ["# Parameters for downsampling"],
}