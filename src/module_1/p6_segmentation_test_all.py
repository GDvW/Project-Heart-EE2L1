from pathlib import Path

from lib.config.ConfigParser import ConfigParser
from src.module_1.p6_segmentation import segmentation

files = list(Path("./samples/").glob("*_realHeart*/recording*.wav"))

config = ConfigParser()

for file in files:
    segmentation(config, str(file), write_results = False)