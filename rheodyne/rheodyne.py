import serial
import time

# Selector
class Rheodyne:
    def __init__(self,port):
        self.serial = serial.Serial(port,timeout=2)
        time.sleep(2) # need to wait for Arduino to reset itself after open
    
    def selector(self,position):
        self.serial.write('S' + str(position-1))
        response = self.serial.readline()
        if not response.startswith('done'):
            self.error('Unexpected response from selector',response)
    
    def valve(self,inject):
        if inject:
            # inject
            self.serial.write('V0')
        else:
            # load
            self.serial.write('V1')
            
        response = self.serial.readline()
        if not response.startswith('done'):
            self.error('Unexpected response from valve',response)          
    
    def close(self):
        self.serial.close()

    def error(*msg):
        print('Error:',msg)