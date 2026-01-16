from __future__ import annotations
from lib.general.generalUtils import randomize

class ValveParams:
    """
    @author: Gerrald
    @date: 10-12-2025
    
    Class to save the various parameter of one valve sound. 
    
    A single valve sound consists two parts: the onset and the main. The onset comes first, the main part after that.
    """
    def __init__(self, delay_ms:float, duration_total_ms: float, duration_onset_ms:float, a_onset: float, a_main: float, 
                         ampl_onset: float,  ampl_main:float, freq_onset:float, freq_main:float, name: str=None):
        """
        @author: Gerrald
        @date: 10-12-2025
        
        Initialize a ValveParams instance.

        Args:
            delay_ms (float): The delay till the sound starts in ms.
            duration_total_ms (float): The total duration (including onset) of the sound in ms.
            duration_onset_ms (float): The duration of the onset of the sound in ms.
            a_onset (float): The gain of the onset. Negative means dampened amplitude, positive exploding amplitude.
            a_main (float): The gain of the main part of the sound. Negative means dampened amplitude, positive exploding amplitude.
            ampl_onset (float): The amplitude of the onset.
            ampl_main (float): The amplitude of the main part.
            freq_onset (float): The frequency of the onset in Hz.
            freq_main (float): The frequency of the main part in Hz.
            name (str, optional): The name of this sound. Defaults to None.
        """
        self.delay = delay_ms / 1000
        self.duration_total = duration_total_ms / 1000
        self.duration_onset = duration_onset_ms / 1000
        self.a_onset = a_onset
        self.a_main = a_main
        self.ampl_onset = ampl_onset
        self.ampl_main = ampl_main
        self.freq_onset = freq_onset
        self.freq_main = freq_main

        self.name = name
    def toStr(self) -> list[str]:
        """
        @author: Gerrald
        @date: 10-12-2025
        
        Returns a string representation of each property of itself in a list.
        
        Returns:
            list[str]: The string representations in a list.
        """
        return [
            f"Name: {self.name}",
            f"  Delay: {self.delay*1000}ms",
            f"  Total duration: {self.duration_total*1000}ms",
            f"  Duration onset: {self.duration_onset*1000}ms",
            f"  A onset: {self.a_onset}",
            f"  A main: {self.a_main}",
            f"  Ampl onset: {self.ampl_onset}",
            f"  Ampl main: {self.ampl_main}",
            f"  Freq onset: {self.freq_onset}Hz",
            f"  Freq main: {self.freq_main}Hz",
        ]
    def properties(self) -> str:
        """
        @author: Gerrald
        @date: 10-12-2025
        
        Returns the names of the properties of itself in a csv-string.

        Returns:
            str: The names of the properties of itself in a csv-string
        """        
        return "name,delay,duration_total,duration_onset,a_onset,a_main,ampl_onset,ampl_main,freq_onset,freq_main"
    def values_str(self) -> list[str]:
        """
        @author: Gerrald
        @date: 10-12-2025
        
        Returns the values of the properties of itself in a list of strings.

        Returns:
            list[str]: The strings representations of the values.
        """
        return list(map(str, self.num_values()))
    def num_values(self) -> list[float]:
        """
        @author: Gerrald
        @date: 10-12-2025
        
        Returns the values of the properties of itself in a list.

        Returns:
            list[float]: The values.
        """
        return [self.delay,self.duration_total,self.duration_onset,self.a_onset,self.a_main,self.ampl_onset,self.ampl_main,self.freq_onset,self.freq_main]
    def __repr__(self) -> str:
        """
        @author: Gerrald
        @date: 14-01-2026
        """
        return "\n".join(self.toStr())
    def randomize(self, ratio: float) -> float:
        """
        @author: Gerrald
        @date: 14/01/2026
        
        Randomize each of its properties a bit.

        Args:
            ratio (float): How much to randomize the parameters as ratio of the property.
        """
        self.delay = randomize(self.delay, ratio/100)
        self.duration_total = randomize(self.duration_total, ratio/100)
        self.duration_onset = randomize(self.duration_onset, ratio/100)
        self.a_onset = randomize(self.a_onset, ratio)
        self.a_main = randomize(self.a_main, ratio)
        self.ampl_onset = randomize(self.ampl_onset, ratio)
        self.ampl_main = randomize(self.ampl_main, ratio)
        self.freq_onset = randomize(self.freq_onset, ratio)
        self.freq_main = randomize(self.freq_main, ratio)
    def store_meta(self, valves: list[ValveParams], mode: str):
        """
        @author: Gerrald
        @date: 14/01/2026
        
        This compares another valve object with this valve and checks if this object is smaller/bigger, and stores it if it is the case
        """
        assert mode in ["min", "max"], "mode should be either 'min' or 'max'"
        f = min if mode == "min" else max
        for valve in valves:
            if self.name == valve.name:
                self.delay = f(self.delay, valve.delay)
                self.duration_total = f(self.duration_total, valve.duration_total)
                self.duration_onset = f(self.duration_onset, valve.duration_onset)
                self.a_onset = f(self.a_onset, valve.a_onset)
                self.a_main = f(self.a_main, valve.a_main)
                self.ampl_onset = f(self.ampl_onset, valve.ampl_onset)
                self.ampl_main = f(self.ampl_main, valve.ampl_main)
                self.freq_onset = f(self.freq_onset, valve.freq_onset)
                self.freq_main = f(self.freq_main, valve.freq_main)