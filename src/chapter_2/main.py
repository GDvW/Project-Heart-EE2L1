import matplotlib.pyplot as plt
from matplotlib import axes
from lib.os.pathutils import getFilesExt
from os.path import exists, join, basename
import pandas as pd
from scipy.io import wavfile
from scipy.fft import fft
import numpy as np

def plot_pcg(file: str, time_ax: axes.Axes = None, freq_ax: axes.Axes =None, title=None):
    """_summary_

    Args:
        file (str): _description_
        time_ax (axes.Axes, optional): _description_. Defaults to None.
        freq_ax (axes.Axes, optional): _description_. Defaults to None.
        title (_type_, optional): _description_. Defaults to None.
    """
    if title is None:
        title = basename(file).split("_")[0]
    Fs, x = wavfile.read(file)
    
    X = fft(x)
    
    t = np.linspace(0, len(x)/Fs, len(x))
    f = np.linspace(0, Fs, len(x))
    
    time_ax.plot(t, x)
    time_ax.set_xlabel("Time [s]")
    time_ax.set_ylabel("Amplitude")
    time_ax.set_title(title)
    
    freq_ax.plot(f, np.abs(X))
    freq_ax.set_xlabel("Frequency [Hz]")
    freq_ax.set_ylabel("Amplitude")
    freq_ax.set_title(title)
    

def main(pcg_dir = "./samples/chapter_2/", csv_data_file = None):
    """_summary_

    Args:
        pcg_dir (str, optional): _description_. Defaults to "./samples/chapter_2/".
        csv_data_file (_type_, optional): _description_. Defaults to None.

    Returns:
        _type_: _description_
    """
    # Get all wav files from the samples directory
    pcgs = getFilesExt(".wav", pcg_dir)
    if csv_data_file is None:
        csv_files = getFilesExt(".csv", pcg_dir)
        if len(csv_files) > 1:
            print("ERROR: multiple csv datafiles. Please specify the correct one using the csv_data_file parameter.")
            return -1
        elif len(csv_files) == 1:
            csv_data_file = join(pcg_dir, csv_files[0])
            print(f"using {csv_files}")
        else:
            print("WARNING: no csv datafile found. Not using any info from the datafile.")
    else:
        if not exists(csv_data_file):
            print("ERROR: csv datafile not found. Please specify a correct one using the csv_data_file parameter.")
            return -1
            
    if csv_data_file is not None:
        data = pd.read_csv(csv_data_file)
    
    numRows = len(pcgs)
    if numRows == 0:
        print(f"ERROR: no wav files found at {pcg_dir}. Exiting.")
        return -1
             
    fig, axes = plt.subplots(len(pcgs), 2, figsize=(8,len(pcgs)*2.5), constrained_layout=True)
    
    for i, pcg in enumerate(pcgs):
        title = basename(pcg).split("_")[0]
        if csv_data_file is not None:
            condition = data.loc[data["Patient ID"] == int(title), "Outcome"].iloc[0]
            title = f"{title} - {condition}"
        plot_pcg(join(pcg_dir, pcg), axes[i][0], axes[i][1], title)
        
    plt.show()
    return 0

if __name__ == "__main__":
    main()