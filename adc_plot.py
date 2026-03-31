import r2r_adc as r2r
import numpy as np
import time
import matplotlib.pyplot as plt  
import os

print("Текущая директория:", os.getcwd())

def plot_voltage_vs_time(time, voltage, max_voltage):
    plt.figure(figsize=(10, 6))
    plt.plot(time, voltage)
    plt.suptitle("График зависимости напряжения на входе АЦП от времени")
    plt.xlabel("Время, с")
    plt.ylabel("Напряжение, В")
    plt.xlim(0, np.max(time) if time else 1)
    plt.ylim(0, max_voltage)
    plt.grid(visible=True)
    plt.savefig("voltage.png", dpi=300, bbox_inches='tight')
    print("График сохранён в voltage.png")
    plt.close()

def plot_sampling_period_hist(time):

    intervals = []
    for i in range(1, len(time)):
        period = time[i] - time[i-1]
        intervals.append(period)
    
    if not intervals:
        print("Недостаточно данных для гистограммы")
        return

    mean_period = np.mean(intervals)
    std_period = np.std(intervals)
    min_period = np.min(intervals)
    max_period = np.max(intervals)
    
    print(f"\nСтатистика периодов дискретизации:")
    print(f"  Среднее: {mean_period:.6f} с")
    print(f"  Стандартное отклонение: {std_period:.6f} с")
    print(f"  Минимум: {min_period:.6f} с")
    print(f"  Максимум: {max_period:.6f} с")

    x_min = min_period * 0.9 
    x_max = max_period * 1.1   
    
    plt.figure(figsize=(10, 6))
    
    plt.hist(intervals, bins=30, edgecolor='black', alpha=0.7)
    
    plt.suptitle("Распределение периодов дискретизации АЦП\n(метод последовательного счета)")
    plt.xlabel("Период дискретизации, с")
    plt.ylabel("Количество измерений")
    plt.xlim(x_min, x_max)  
    plt.grid(visible=True, linestyle='--', alpha=0.7, axis='y')

    plt.axvline(mean_period, color='red', linestyle='--', linewidth=2, 
               label=f'Среднее: {mean_period:.6f} с')
    plt.legend()
    
    plt.savefig("hist.png", dpi=300, bbox_inches='tight')
    print("Гистограмма сохранена в hist.png")
    plt.close()

adc = r2r.R2R_ADC(3.177, compare_time=0.0001)

voltage_vals = []
time_vals = []
duration = 10

try:
    begin_time = time.time_ns()
    print(f"Начинаю сбор данных в течение {duration} секунд...")
    
    while (time.time_ns() - begin_time) / 1e9 < duration:
        volt = adc.get_sc_voltage()
        current_time = (time.time_ns() - begin_time) / 1e9
        print(f"Время: {current_time:.3f} с, Напряжение: {volt:.3f} В")
        time_vals.append(current_time)
        voltage_vals.append(volt)

    if len(time_vals) > 1:
        print(f"\nСбор данных завершён. Всего измерений: {len(time_vals)}")
        
        print("Создаю график напряжения...")
        plot_voltage_vs_time(time_vals, voltage_vals, np.max(voltage_vals))
        
        print("Создаю гистограмму периодов...")
        plot_sampling_period_hist(time_vals)
        
        print("\nГрафики сохранены. Проверьте папку:")
        print(os.getcwd())
    else:
        print("Недостаточно данных для построения графиков")

finally:
    adc.deinit()
    print("Завершение работы")

