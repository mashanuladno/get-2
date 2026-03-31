import RPi.GPIO as GPIO
import time

class R2R_ADC:
    def __init__(self, dynamic_range, compare_time = 0.01, verbose = False):
        self.dynamic_range = dynamic_range
        self.verbose = verbose
        self.compare_time = compare_time
        
        self.bits_gpio = [26, 20, 19, 16, 13, 12, 25, 11]
        self.comp_gpio = 21

        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits_gpio, GPIO.OUT, initial = 0)
        GPIO.setup(self.comp_gpio, GPIO.IN)

    def deinit(self):
        GPIO.output(self.bits_gpio, 0)
        GPIO.cleanup()
    
    def number_to_dac(self, number):
        GPIO.output(self.bits_gpio, [int(element) for element in bin(number)[2:].zfill(8)])

    def get_sc_voltage(self):
        digital_value = self.sequential_counting_adc()
        
        if digital_value > 0:
            actual_digital = digital_value - 1
        else:
            actual_digital = 0

        voltage = (actual_digital / 255.0) * self.dynamic_range

        return voltage

    def successive_approximation_adc(self):

        low = 0
        high = 255
        guess = 0

        for bit in range(7, -1, -1): 

            guess |= (1 << bit)
  
            self.number_to_dac(guess)
            time.sleep(self.compare_time)

            comparator_output = GPIO.input(self.comp_gpio)
            
            if comparator_output == 1:
                guess &= ~(1 << bit) 

        return guess

    def get_sar_voltage(self):

        digital_value = self.successive_approximation_adc()
  
        voltage = (digital_value / 255.0) * self.dynamic_range

        return voltage

if __name__ == "__main__":
    try:

        DAC_DYNAMIC_RANGE = 3.297
        
        adc = R2R_ADC(dynamic_range=DAC_DYNAMIC_RANGE, 
                     compare_time=0.01, 
                     verbose=True)

        while True:
            voltage = adc.get_sar_voltage()
            print(f"Входное напряжение: {voltage:.3f} В")
            
            time.sleep(0.5)

        
    finally:
        adc.deinit()
