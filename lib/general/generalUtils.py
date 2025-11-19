from math import log10
#wrt to 1
def todB(value: float, power: bool = True):
    return 10 * log10(value) * (1 if power else 2)
    
def fromdB(dB: float, power: bool = True):
    return 10 ** (dB / (10 if power else 20))