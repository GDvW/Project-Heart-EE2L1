from lib.localization.TUI import main as main_tui
from lib.samples.Samples import GENERATED_MODEL_SAMPLES

sample = GENERATED_MODEL_SAMPLES["S1"][0]

print(f"Using {sample.name}")

main_tui(sample)