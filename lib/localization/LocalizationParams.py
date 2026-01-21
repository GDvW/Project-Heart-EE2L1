from dataclasses import dataclass
from typing import Literal

@dataclass
class LocalizationParams:
    bin: int
    z: float
    Fs: int
    Q: int
    M: int
    v_sound: float
    d: float
    resolution: float
    mode: Literal["music", "mvdr"]
    
    def is_scan_points_updated(self, old):
        return self.resolution != old.resolution or self.z != old.z
    def is_bin_updated(self, old):
        return self.bin != old.bin