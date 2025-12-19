import matplotlib.pyplot as plt
import numpy as np

from lib.config.ConfigParser import ConfigParser
from lib.processing.Executor import Executor, Result
from lib.plot.timeFrequencyPlot import *
from lib.plot.plotUtils import *
from lib.general.Result import Result

def testingfunction(config):
    """
    @author: Gerrald
    @date: 10-12-2025
    """
    executor = Executor("samples\\piezo_4_realHeart", config, True)
    executor.execute(write_enabled=False)
    fig, ax = plt.subplots(3, 2, figsize=(16,16), sharex="all", sharey="all", constrained_layout=True)
    for file, values, plot in zip(executor.results.keys(), executor.results.values(), np.array(ax).flatten()):
        processor = values[3]
        status = values[4]
        timeFrequencyPlot(
            processor.see_normalized,
            config.Downsampling.FsTarget,
            plot,
            None,
        )
        plot.scatter(processor.s1_peaks[:,0] / processor.Fs_target, processor.see_normalized[processor.s1_peaks[:,0]], c="red", marker="^", label="S1")
        plot.scatter(processor.s2_peaks[:,0] / processor.Fs_target, processor.see_normalized[processor.s2_peaks[:,0]], c="green", marker="^", label="S2")
        plot.scatter(processor.ind_s1.flatten() / processor.Fs_target, processor.see_normalized[processor.ind_s1.flatten()], c="orange", marker="v", label="S1 ind")
        plot.scatter(processor.ind_s2.flatten() / processor.Fs_target, processor.see_normalized[processor.ind_s2.flatten()], c="darkgrey", marker="v", label="S2 ind")
        
        if status == Result.Success:
            scatter_constant(processor.attention_segments["s1_added"], -0.5, plot, c="green",label="S1 added", marker=">", scaleX=1/processor.Fs_target)
            scatter_constant(processor.attention_segments["s2_added"], -0.5, plot, c="green",label="S2 added", marker="<", scaleX=1/processor.Fs_target)
            scatter_constant(processor.attention_segments["s1_removed"], -0.5, plot, c="red",label="S1 removed", marker=">", scaleX=1/processor.Fs_target)
            scatter_constant(processor.attention_segments["s2_removed"], -0.5, plot, c="red",label="S2 removed", marker="<", scaleX=1/processor.Fs_target)
        
        plot.axhline(y=processor.actual_segmentation_min_height, label="Cutoff")
        plot.axhline(y=processor.segmentation_threshold, label="Threshold", color="green")
        plot.legend()
    plt.show()

def main():
    """
    @author: Gerrald
    @date: 10-12-2025

    The main loop. Can be changed to choose whether to run assignment 4.2.2 or 4.2.3.
    
    """
    config = ConfigParser()
    testingfunction(config)

if __name__ == "__main__":
    main()