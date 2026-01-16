import numpy as np
import matplotlib.pyplot as plt
from os.path import join
from pathlib import Path

from lib.model.Model_3D import Model_3D, Point
from lib.config.ConfigParser import ConfigParser
from lib.model.Model import Model
from lib.processing.Executor import Executor

SUB_FOLDER = "S1+S2 final"

config = ConfigParser()
Fs = config.HeartSoundModel.Fs


base_folder = Path(join(config.Generation.SoundsPath, "3d-model", SUB_FOLDER))
count = sum(1 for _ in base_folder.glob("*.wav"))
if count > 0:
    print(f"Do you want to delete {count} files in {base_folder}? [y/N]")
    answer = input("> ")
    if answer.lower() == "y":
        for file in base_folder.glob("*.wav"):
            file.unlink(missing_ok=True)

model = Model(config, randomize_enabled=False, simulate_S2=True)
model.import_csv(".\\src\\module_2\\model_params.csv")
model.set_n(config.HeartSoundModel.NBeats)
mic_locs = [Point(2.5, 5, 0), # 0
            Point(2.5, 10, 0), # 1
            Point(2.5, 15, 0), # 2
            Point(7.5, 5, 0), # 3
            Point(7.5, 10, 0), # 4
            Point(7.5, 15, 0)]
source_locs = [Point(-1,8,-15),#Order: MTAP
                Point(3,12,-15),
                Point(6,14,-15),
                Point(7,9,-15)]
signals = []
for valve, source in zip (model.valves, source_locs):
    model.valves = [valve]
    t_model, heart_sound = model.generate_model()
    signals.append(heart_sound)

model = Model_3D(config, source_locs, mic_locs)
model.generate(signals)
model.save(SUB_FOLDER)
print("Wrote files, segmenting...")
executor = Executor(base_folder, config, True)
executor.execute(write_enabled=True)
executor.summarize()

