import r2r_dac as r2r
import signal_gen as sg
import time

ampl = 3.0
freq = 1
samp_freq = 1000

try:
    dac = r2r.R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], ampl, True)
    while True:
        try:
            dac.set_vol(sg.get_sin_wave_ampl(freq, time.time()) * ampl)
            sg.wait_for_sampling_period(samp_freq)
        except ValueError:
            print("smth went wrong wow\n")
finally:
    dac.set_vol(0)
    dac.deinit()
