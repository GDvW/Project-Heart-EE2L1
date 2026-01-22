from lib.localization.TUI import main as main_tui
from lib.samples.Samples import SAMPLES

# sample = SAMPLES["Phantom"][0]
sample = SAMPLES["Generated"][0]

print(f"Using {sample.name}")

main_tui(sample)