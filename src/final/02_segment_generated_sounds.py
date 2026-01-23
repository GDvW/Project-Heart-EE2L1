import matplotlib.pyplot as plt

from lib.config.ConfigParser import ConfigParser
from lib.processing.Executor import Executor
from lib.samples.Samples import SAMPLES_SELF_CALIBRATED

def main():
    """
    @author: Gerrald
    @date: 23/01/2026
    """
    plt.ion()
    sample = SAMPLES_SELF_CALIBRATED["Real"][0]
    i = 0
    failed = []
    for sample in SAMPLES_SELF_CALIBRATED["Real"]:
        try:
            config = ConfigParser()
            # executor = Executor("generated\\hearbeat model\\3d-model\\HeartSimulation", config, output_subfolder="3D model heartsimulation", log=True)
            executor = Executor(sample.root, config, output_subfolder=f"RealPatients/{sample.root.stem}", log=True)
            executor.execute()
            executor.summarize()
        except Exception as e:
            print(f"CRITICAL: {sample} -> {e}")
            failed.append(f"CRITICAL: {sample} -> {e}")
        i+=1
    print("#"*100, i)
    print("\n\n\n".join(failed))

if __name__ == "__main__":
    main()