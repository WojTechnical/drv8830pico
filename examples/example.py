import machine, time
from machine import Pin

import drv8830pico

sda=machine.Pin(0)
scl=machine.Pin(1)

drv = drv8830pico.DRV8830(sda_pin=sda, scl_pin=scl)

#set voltage appropriate for your motor
drv.SetVoltage(3)

#drive forward for 5 seconds
drv.ClearFaults()
drv.Forward()
faults = drv.CheckFaults()
if len(faults) > 0:
    raise Exception("Motor fault detected: " + faults)
time.sleep(5)

#stop and pause for a second
drv.ClearFaults()
drv.Brake()
faults = drv.CheckFaults()
if len(faults) > 0:
    raise Exception("Motor fault detected: " + faults)
time.sleep(1)

#drive backwards for 5 seconds
drv.ClearFaults()
drv.Backward()
faults = drv.CheckFaults()
if len(faults) > 0:
    raise Exception("Motor fault detected: " + faults)
time.sleep(5)

#coast to a stop
drv.ClearFaults()
drv.Coast()
faults = drv.CheckFaults()
if len(faults) > 0:
    raise Exception("Motor fault detected: " + faults)