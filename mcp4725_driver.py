import smbus
import RPi.GPIO as GPIO

class MCP4725:
    def __init__(self, drange, address = 0x61, verbose = False):
        self.bus = smbus.SMBus(1)
        self.range = drange
        self.address = address
        self.wm = 0x00
        self.pds = 0x00
        self.verbose = verbose
        
    def deinit(self):
        self.bus.close()
        
    def set_num(self, number):
        if not isinstance(number, int):
            print("Integers only!")
            return
        if not (0 <= number <= 4095):
            print("Out of range! [0..4095]")
            return
        
        first_byte = self.wm | self.pds | number >> 8
        second_byte = number & 0xFF
        self.bus.write_byte_data(0x61, first_byte, second_byte)
        
        if self.verbose:
            print(f"Num: {number}, data sent to I2C: [0x{(self.address << 1):02X}, 0x{first_byte:02X}, 0x{second_byte:02X}]\n")
    
    def set_vol(self, voltage):
        if not (0.0 <= voltage <= self.range):
            if self.verbose:
                print(f"Out of range 0.00-{self.range:.2f} V")
            self.set_num(0)
            return
        self.set_num(int(voltage / self.range * 4095))
        
if __name__ == "__main__":
    try:
        dac = MCP4725(3.12, verbose = True)
        
        while True:
            try:
                vol = float(input("Input voltage (in volts)"))
                dac.set_vol(vol)
            
            except ValueError:
                print("Incorrect input! Try again\n")
    finally:
        dac.deinit()
