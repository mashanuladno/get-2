import r2r_adc as r2r
import time
import matplotlib.pyplot as plt
import numpy as np

adc = r2r.R2R_ADC(3.3, compare_time=0.0001)

voltage_vals = []
time_vals = []
duration = 3.0

try:
    begin_time = time.time_ns()
    print(f"Начинаю сбор данных в течение {duration} секунд...")

    while (time.time_ns() - begin_time) / 1e9 < duration:
        volt = adc.get_sc_voltage()
        current_time = (time.time_ns() - begin_time) / 1e9
        print(f"Время: {current_time:.3f} с, Напряжение: {volt:.3f} В")
        time_vals.append(current_time)
        voltage_vals.append(volt)
