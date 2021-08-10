import machine
import sys

__version__ = '1.0'

I2C_ADDR1 = 0x60  # Default, both select jumpers bridged (not cut)
I2C_ADDR2 = 0x61  # Cut A0
I2C_ADDR3 = 0x63  # Cut A1
I2C_ADDR4 = 0x64  # Cut A0 and A1

MOTOR_FORWARD = 0b10
MOTOR_BACKWARD = 0b01
MOTOR_BRAKE = 0b11
MOTOR_COAST = 0b00

CONTROL_REGISTER_ADDR = 0x00
ERROR_REGISTER_ADDR = 0x01

ERROR_FAULT_BIT = 0b1
ERROR_OCP_BIT = 0b01
ERROR_UVLO_BIT = 0b001
ERROR_OTS_BIT = 0b0001
ERROR_ILIMIT_BIT = 0b00001
ERROR_CLEAR_FAULTS_BIT = 0b10000000

DEBUG_PRINT = True

class DRV8830:

    #Voltage to index calculation taken from Pimoroni's own library here: https://github.com/pimoroni/drv8830-python
    def VoltageToIndex(self, voltage):
        if voltage < 0.48 or voltage > 5.06:
            raise ValueError("Incorrect voltage for motor controller")
        offset = -0.01 if voltage >= 1.29 else 0
        offset -= 0.01 if voltage >= 3.86 else 0
        return int(offset + voltage / 0.08)
        
    def __init__(self, sda_pin, scl_pin, i2c_addr=I2C_ADDR1, i2c_id=0):
        self._i2c_addr = i2c_addr
        self.control_register = 0b00000000
        self.error_register = 0b00000000
        self.current_direction = MOTOR_BRAKE
        self.current_voltage = 0x00
        self.i2c_device = machine.I2C(id=i2c_id,sda=sda_pin, scl=scl_pin, freq=400000)
        self.ClearFaults()

    def WriteControlRegister(self):
        self.control_register = self.current_voltage << 2
        self.control_register |= self.current_direction
        self.i2c_device.writeto_mem(self._i2c_addr, CONTROL_REGISTER_ADDR, self.control_register.to_bytes(1, sys.byteorder))
        if DEBUG_PRINT:
            print("current voltage: " + bin(self.current_voltage))
            print("current direction: " + bin(self.current_direction))
            print("control register: " + bin(self.control_register))

    def SetVoltage(self, voltage):
        if DEBUG_PRINT:
            print("Setting voltage: " + str(voltage))
        self.current_voltage = self.VoltageToIndex(voltage)
        self.WriteControlRegister()

    def Forward(self):
        if DEBUG_PRINT:
            print("Setting motor to move forward")
        self.current_direction = MOTOR_FORWARD
        self.WriteControlRegister()

    def Backward(self):
        if DEBUG_PRINT:
            print("Setting motor to move backward")
        self.current_direction = MOTOR_BACKWARD
        self.WriteControlRegister()

    def Coast(self):
        if DEBUG_PRINT:
            print("Setting motor to coast")
        self.current_direction = MOTOR_COAST
        self.WriteControlRegister()
    
    def Brake(self):
        if DEBUG_PRINT:
            print("Setting motor to brake")
        self.current_direction = MOTOR_BRAKE
        self.WriteControlRegister()

    def ClearFaults(self):
        if DEBUG_PRINT:
            print("Clearing faults on controller")
        self.i2c_device.writeto_mem(self._i2c_addr, ERROR_REGISTER_ADDR, ERROR_CLEAR_FAULTS_BIT.to_bytes(1, sys.byteorder))

    def CheckFaults(self):
        self.error_register = self.i2c_device.readfrom_mem(self._i2c_addr, ERROR_REGISTER_ADDR, 1)
        error_register_as_int = int.from_bytes(self.error_register, sys.byteorder)
        faults_found = []

        if error_register_as_int & ERROR_FAULT_BIT: #if the fault bit is set, then check for specific faults
            if error_register_as_int & ERROR_OCP_BIT:
                faults_found.append("Overcurrent event")
            if error_register_as_int & ERROR_UVLO_BIT:
                faults_found.append("Undervoltage lockout")
            if error_register_as_int & ERROR_OTS_BIT:
                faults_found.append("Overtemperature condition")
            if error_register_as_int & ERROR_ILIMIT_BIT:
                faults_found.append("Extended current limit event")

        if DEBUG_PRINT:
            if len(faults_found) > 0:
                print("Faults found:")
                for fault in faults_found:
                    print(fault)

        return faults_found