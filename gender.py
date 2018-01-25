#!/usr/bin/python

import sys
import glob
from matplotlib.mlab import find
from scipy.io import wavfile
from numpy import *
from scipy.signal import fftconvolve

def calculate_freq(signal, fs):
    correlation = fftconvolve(signal, signal[::-1], mode='full')
    correlation = correlation[int(len(correlation)/2):]
    try:
        first_low = find(diff(correlation) > 0)[0]
        peak = argmax(correlation[first_low:]) + first_low
        return fs / peak
    except:
        return -1


def main(filename):
    try:
        fs, data = wavfile.read(filename) # load the data
    except:
        print("Could not read the file")
        return
    signal = data.T# this is a two channel soundtrack, I get the first track
    if data.T.ndim>1:
        signal = data.T[0]
    results=[]
    for i in range(0,len(signal)//6000):
        result=calculate_freq(signal[6000*i:min((6000*(i+1)),len(signal))],fs)
        if 60 < result < 400:
            results.append(result)
    result=median(results)
    if(result<170):
       print("M")
    else:
       print("F")
if __name__ == "__main__":
    main(sys.argv[1])
