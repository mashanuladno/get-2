import RPi.GPIO as GPIO

class PWM_DAC:
    def __init__(self, bits, freq, drange, verbose = False):
        self.bits = bits
        self.freq = freq
        self.range = drange
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits, GPIO.OUT, initial = 0)
        
        self.pwm = GPIO.PWM(self.bits, self.freq)
        self.pwm.start(0)
        
    def deinit(self):
        self.pwm.stop()
        GPIO.output(self.bits, 0)
        GPIO.cleanup()
    
    def set_vol(self, voltage):
        if not (0.0 <= voltage <= self.range):
            if self.verbose:
                print(f"Out of range 0.00-{self.range:.2f} V")
            self.pwm.ChangeDutyCycle(0)
            return
        self.pwm.ChangeDutyCycle(int(voltage / self.range * 100))
        
if __name__ == "__main__":
    try:
        dac = PWM_DAC(12, 500, 3.290, True)
        
        while True:
            try:
                vol = float(input("Input voltage (in volts)"))
                dac.set_vol(vol)
            
            except ValueError:
                print("Incorrect input! Try again\n")
    finally:
        dac.deinit()
