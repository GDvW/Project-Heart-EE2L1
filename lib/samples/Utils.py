from pathlib import Path

def get_recordings(root: str|Path):
    return list({
        file.parent
        for file in Path(root).rglob("*.wav")
    })
    
if __name__ == "__main__" :
    from lib.config.ConfigParser import ConfigParser
    config = ConfigParser()
    print(get_recordings(config.Recordings.UncalibratedPath))