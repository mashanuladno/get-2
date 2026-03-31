import RPi.GPIO as GPIO


GPIO.setmode(GPIO.BCM)
dac = [16, 20, 21, 25, 26, 17, 27, 22]
GPIO.setup(dac, GPIO.OUT)

dynamic_range = 3.18

def vol2num(voltage):
    if not (0.0 <= voltage <= dynamic_range):
        print(f"Out of range 0.00-{dynamic_range:.2f} V")
        return 0
    return int(voltage / dynamic_range * 255)

def num2dac(dac, number):
    GPIO.output(dac, [int(element) for element in bin(number)[2:].zfill(8)])

try:
    while True:
        try:
            vol = float(input("Input voltage (in volts)"))
            number = vol2num(vol)
            num2dac(dac, number)
            
        except ValueError:
            print("Incorrect input! Try again\n")
finally:
    GPIO.output(dac, 0)
    GPIO.cleanup()
    GPIO.output(dac_bits, 0)
    GPIO.cleanup()
