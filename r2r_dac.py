import RPi.GPIO as GPIO

class R2R_DAC:
    def __init__(self, bits, drange, verbose = False):
        self.bits = bits
        self.range = drange
        self.verbose = verbose
        
        GPIO.setmode(GPIO.BCM)
        GPIO.setup(self.bits, GPIO.OUT, initial = 0)
        
    def deinit(self):
        GPIO.output(self.bits, 0)
        GPIO.cleanup()
        
    def set_num(self, number):
        GPIO.output(self.bits, [int(element) for element in bin(number)[2:].zfill(8)])
    
    def set_vol(self, voltage):
        if not (0.0 <= voltage <= self.range):
            if self.verbose:
                print(f"Out of range 0.00-{self.range:.2f} V")
            self.set_num(0)
            return
        self.set_num(int(voltage / self.range * 255))
        

if __name__ == "__main__":
    try:
        dac = R2R_DAC([16, 20, 21, 25, 26, 17, 27, 22], 3.183, True)
        
        while True:
            try:
                vol = float(input("Input voltage (in volts)"))
                dac.set_vol(vol)
            
            except ValueError:
                print("Incorrect input! Try again\n")
    finally:
        dac.deinit()
