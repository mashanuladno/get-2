import numpy
import time

def get_sin_wave_ampl(freq, t):
    return (numpy.sin(2 * numpy.pi * freq * t) + 1) / 2

def wait_for_sampling_period(sampling_freq):
    time.sleep(1/sampling_freq)
