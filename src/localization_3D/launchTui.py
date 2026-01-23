from lib.localization.TUI import main as main_tui
from lib.samples.Samples import SAMPLES_CALIBRATED, SAMPLES_SELF_CALIBRATED

# sample = SAMPLES_CALIBRATED["Phantom"][0]
# sample = SAMPLES_CALIBRATED["Generated"][0]
# sample = SAMPLES_SELF_CALIBRATED["Phantom"][5]
sample = SAMPLES_SELF_CALIBRATED["Real"][3]

print(f"Using {sample.name}")

main_tui(sample)