#test stepper using motor HAT 

#continuously move stepper motor 

 

import time 

from adafruit_motorkit import MotorKit 

from adafruit_motor import stepper 

 

kit = MotorKit(address=0x6f) 

 

for i in range(3000): 

    kit.stepper1.onestep() 

    time.sleep(0.01) 