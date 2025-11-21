from lib.processing.functions import *
from lib.config.ConfigParser import ConfigParser
from scipy.io import wavfile

class Processor:
    """Wrapper for the processing stage.
    
    This class allows to easily reuse code across the whole codebase and optionally save results for plotting them.
    """
    def __init__(self, file_path: str, config: ConfigParser, save_results: bool = False):
        """Initializes the processor.

        Args:
            file_path (str): The path to the wav file.
            config (ConfigParser): The config object.
            save_results (bool, optional): Whether to save the substeps. Defaults to False.
        """
        # Save path to wav file
        self.file_path = file_path
        
        # Retrieve config values
        self.lp_low_freq = config.LowpassFilter.LowFrequency
        self.lp_high_freq = config.LowpassFilter.HighFrequency
        self.lp_filter_order = config.LowpassFilter.FilterOrder
        self.lp_filter_size = config.LowpassFilter.Size
        self.Fs_target = config.Downsampling.FsTarget
        
        self.save_results = save_results
        # Initialize fields that values can be saved to
        self.Fs_original = None
        self.x = None
        self.g = None
        self.y = None
        self.y_downsampled = None
    def process(self):
        """Initialize the processing and optionally save the steps in between.
        """
        Fs_original, x = wavfile.read(self.file_path)
    
        g = construct_filter(self.lp_low_freq, self.lp_high_freq, Fs_original, order=self.lp_filter_order, size=self.lp_filter_size)
        
        y = filter(x, g)
        
        y_downsampled = downsample(x, Fs_original, self.Fs_target)
        
        if self.save_results:
            self.Fs_original = Fs_original
            self.x = x
            self.g = g
            self.y = y
            self.y_downsampled = y_downsampled