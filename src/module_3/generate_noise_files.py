from scipy.io.wavfile import write
import winsound
import wave 
import os
import numpy as np

Fs = 48000
signal1 = np.random.randint(-5000, 5000, 10*Fs).astype(np.int16).reshape(-1,1)
signal2 = np.random.randint(-5000, 5000, 10*Fs).astype(np.int16).reshape(-1,1)
signalsource1 = np.concatenate((signal1, signal2), axis=1)
write("file_src1.wav", Fs, signalsource1) #double source wav file

print (signalsource1.shape)
print (signalsource1)
print ("okay1")

zeroed_s1 = np.zeros(len(signal1)).astype(np.int16).reshape(-1,1)
signalsource2 = np.concatenate((zeroed_s1, signal2), axis =1)

print (signalsource2.shape)
print (signalsource2)
print ("okay2")
write("file_src2.wav", Fs, signalsource2) #single source wav file

signalsource3 = np.concatenate((signal2, zeroed_s1), axis =1)
print (signalsource3.shape)
print (signalsource3)
print ("okay3")
write("file_src3.wav", Fs, signalsource3) #single source wav file


#winsound.PlaySound("file_src1.wav", winsound.SND_FILENAME)
#winsound.PlaySound("file_src2.wav", winsound.SND_FILENAME)
