import smbus
import time
import matplotlib.pyplot as plt
import numpy as np

class MCP3021:
    def __init__(self, dynamic_range, address=0x4D, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = address
        self.verbose = verbose
        
    def deinit(self):
        self.bus.close()
        
    def get_number(self):
        try:
            data = self.bus.read_word_data(self.address, 0)
            value = ((data & 0xFF) << 8) | ((data >> 8) & 0xFF)
            number = value >> 2
            return number
        except Exception as e:
            print(f"Ошибка чтения I2C: {e}")
            return 0
        
    def get_voltage(self):
        digital_value = self.get_number()
        voltage = (digital_value / 1023.0) * self.dynamic_range
        return voltage


if __name__ == "__main__":
    ADC_DYNAMIC_RANGE = 3.297  
    
    adc = MCP3021(dynamic_range=ADC_DYNAMIC_RANGE, address=0x4D, verbose=False)
    
    voltage_values = []
    time_values = []
    duration = 10.0
    
    try:
        start_time = time.time()
        
        while (time.time() - start_time) < duration:
            current_time = time.time() - start_time
            voltage = adc.get_voltage()
            
            voltage_values.append(voltage)
            time_values.append(current_time)
            
            print(f"Время: {current_time:.3f} с, Напряжение: {voltage:.3f} В")
            
        plt.figure(figsize=(10, 6))
        plt.plot(time_values, voltage_values)
        plt.title("Зависимость напряжения от времени")
        plt.xlabel("Время, с")
        plt.ylabel("Напряжение, В")
        plt.grid(True)
        plt.savefig("voltage_plot.png", dpi=300, bbox_inches='tight')
        print("График напряжения сохранён в voltage_plot.png")
        plt.close()
        
        intervals = []
        for i in range(1, len(time_values)):
            period = time_values[i] - time_values[i-1]
            intervals.append(period)
        
        if intervals:
            plt.figure(figsize=(10, 6))
            plt.hist(intervals, bins=30, edgecolor='black', alpha=0.7)
            plt.title("Распределение периодов дискретизации")
            plt.xlabel("Период, с")
            plt.ylabel("Количество измерений")
            plt.grid(True, alpha=0.3)
            plt.savefig("histogram.png", dpi=300, bbox_inches='tight')
            print("Гистограмма сохранена в histogram.png")
            plt.close()
            
    except KeyboardInterrupt:
        print("\nПрограмма остановлена")
    finally:
        adc.deinit()
