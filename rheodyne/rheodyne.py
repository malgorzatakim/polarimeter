from __future__ import print_function 
import serial
import time

# Selector
class Rheodyne:
    def __init__(self,port):
        self.serial = serial.Serial(port,timeout=2)
        time.sleep(2) # need to wait for Arduino to reset itself after open
        if self.serial.isOpen():
            print('Rheodyne: created on',port)
        else:
            error('Rheodyne: ERROR - not opened on',port)

    
    def selector(self,position):
        self.serial.write('S' + str(position-1))
        response = self.serial.readline()
        if not response.startswith('done'):
            self.error('Rheodyne: unexpected response from selector',response)
        else:
            print('Rheodyne: selector set to',position)

    def valve(self,inject):
        if inject:
            # inject
            self.serial.write('V0')
            status = 'inject'
        else:
            # load
            self.serial.write('V1')
            status = 'load'
            
        response = self.serial.readline()
        if not response.startswith('done'):
            self.error('Rheodyne: unexpected response from valve',response)
        else:
            print('Rheodyne: six port set to ',status)
    
    def close(self):
        self.serial.close()
        if not self.serial.isOpen():
            print('Rheodyne: serial port closed OK')
        else:
            print('Rheodyne: ERROR - serial port not closed')

    def error(*msg):
        print('Error:',msg)