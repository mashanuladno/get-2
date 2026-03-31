import pwm_dac as pwm
import signal_gen as sg
import time

ampl = 2.0
freq = 100
samp_freq = 500

try:
    dac = pwm.PWM_DAC(12, 5000, 3.290, True)
    state = 0
    max_state = 100
    step = 1
    sign = 1
    while True:
        try:
            dac.set_vol(state * ampl / max_state)
            sg.wait_for_sampling_period(samp_freq)
            state += step * sign
            if state >= max_state or state <= 0:
                if sign == 1:
                    sign = -1
                else:
                    sign = 1
        except ValueError:
            print("smth went wrong wow\n")
finally:
    dac.deinit()
