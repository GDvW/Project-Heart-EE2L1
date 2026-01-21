from dataclasses import dataclass, fields
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

    def print_filename(self):
        print(self.to_filename(ext="png"))
        
    def to_filename(self, prefix="LocalizationParams", ext=""):
        parts = []
        for f in fields(self):
            key = f.name
            val = getattr(self, key)

            # Convert value to string
            s = str(val)

            # Remove characters that are unsafe in filenames
            safe = (
                s.replace(" ", "")
                 .replace("(", "")
                 .replace(")", "")
                 .replace(",", "")
                 .replace("=", "")
                 .replace("'", "")
                 .replace('"', "")
            )

            parts.append(f"{key}{safe}")

        filename = prefix + "_" + "_".join(parts)
        if ext:
            filename += f".{ext.lstrip('.')}"
        return filename
