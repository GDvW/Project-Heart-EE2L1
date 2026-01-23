from lib.localization.TUI import main as main_tui
from lib.samples.Samples import GENERATED_MODEL_SAMPLES, SEGMENTED_REAL_DATA

# sample = GENERATED_MODEL_SAMPLES["S1"][0]
# sample = GENERATED_MODEL_SAMPLES["S2"][0]
sample = SEGMENTED_REAL_DATA["S1"][1]

print(f"Using {sample.name}")

main_tui(sample)