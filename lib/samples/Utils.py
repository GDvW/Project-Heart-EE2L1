from pathlib import Path
import re
from enum import Enum, auto

class RecordingsCount(Enum):
    BOTTOM = auto()
    TOP = auto()
    NONE = auto()
    BOTH = auto()
    UNCERTAIN_BUT_TWO = auto()
    def from_left_right(left: bool, right: bool):
        match left + right:
            case 0:
                return RecordingsCount.NONE
            case 1:
                if left: return RecordingsCount.TOP
                return RecordingsCount.BOTTOM
            case 2:
                return RecordingsCount.BOTH
    def to_int(self):
        match self:
            case RecordingsCount.NONE:
                return 0
            case RecordingsCount.BOTTOM | RecordingsCount.TOP:
                return 1
            case RecordingsCount.BOTH | RecordingsCount.UNCERTAIN_BUT_TWO:
                return 2
    

def get_recordings(root: str|Path):
    return list({
        file.parent
        for file in Path(root).rglob("*.wav")
    })
    
# hole-locations should be ordered small y to large y
def createSampleList(root: str|Path):
    recordings = get_recordings(root)
    result = {
        "phantom": "",
        "real": ""
    }
    for recording in recordings:
        m = re.search(r"\(([^)]+) +([^)]+)\)", recording.stem)
        filename = f"{m.group(1)}_{m.group(2)}" if m else recording.stem
        match recording.parent.stem:
            case "phantom":
                folder = "config.Recordings.PhantomMap"
                key = "phantom"
            case "real":
                folder = "config.Recordings.RealMap"
                key = "real"
            case _:
                print(f"Unknown folder {recording.parent.stem}")
                continue
        if m:
            count = RecordingsCount.from_left_right(m.group(1).strip() != "silent", m.group(2).strip() != "silent")
        else:
            count = RecordingsCount.UNCERTAIN_BUT_TWO
            
        match count.to_int():
            case 0:
                hole_locations = "np.array([])"
            case 1:
                if count == RecordingsCount.BOTTOM:
                    hole_locations = "np.array([hole_locations[0]])"
                else: # RecordingsCount.TOP
                    hole_locations = "np.array([hole_locations[1]])"
            case 2:
                if count == RecordingsCount.BOTH:
                    hole_locations = "hole_locations"
                else: # RecordingsCount.UNCERTAIN_BUT_TWO
                    hole_locations = "np.array([])"
            
        result[key] += f"""Sample(
    "{recording.parent.stem}_{filename}",
    Path(config.Recordings.SoundsPath).joinpath({folder}, "{recording.stem}"),
    0.015,
    {count.to_int()},
    standard_mic_locations,
    {hole_locations}
),\n"""
    return result
    
    
if __name__ == "__main__" :
    from lib.config.ConfigParser import ConfigParser
    config = ConfigParser()
    # print(get_recordings(config.Recordings.UncalibratedPath))
    result = createSampleList(config.Recordings.SoundsPath)
    print("PHANTOM-----------------------------------------------------------")
    print(result["phantom"])
    print("REAL--------------------------------------------------------------")
    print(result["real"])