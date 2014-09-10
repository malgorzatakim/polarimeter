from __future__ import print_function 
import serial
import time
import argparse
import logging

# Selector
class Rheodyne:
    def __init__(self,port):
        self.serial = serial.Serial(port,timeout=2)
        time.sleep(2) # need to wait for Arduino to reset itself after open
        if self.serial.isOpen():
            logging.info('Rheodyne: opened on %s',port)
        else:
            logging.error('Rheodyne: could not open on %s',port)

    def selector(self,position):
        if position > 0 and position < 11:
            self.serial.write('S' + str(position-1))
            response = self.serial.readline()
            if not response.startswith('done'):
                logging.error('Rheodyne: unexpected response from selector')
            else:
                logging.info('Rheodyne: selector set to %s',position)
        else:
            logging.error('Rheodyne: %s is an invalid position',position)

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
            logging.error('Rheodyne: unexpected response from valve')
        else:
            logging.info('Rheodyne: six port %s',status)
    
    def close(self):
        self.serial.close()
        if not self.serial.isOpen():
            logging.info('Rheodyne: serial port closed')
        else:
            logging.error('Rheodyne: could not close serial port')

# Command line options
# Run with -h flag to see help

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Command line interface to control Rheodyne six-port and selector valve via an Arduino')
    parser.add_argument('port',help='serial port')
    # selector
    parser.add_argument('-s',dest='selector',help='selector position',type=int)
    group = parser.add_mutually_exclusive_group()
    # six port
    group.add_argument('-inject',action='store_true')
    group.add_argument('-load',action="store_true")
    args = parser.parse_args()

    rheo = Rheodyne(args.port)

    if args.selector:
        rheo.selector(args.selector)

    if args.inject:
        rheo.valve(True)
    elif args.load:
        rheo.valve(False)

    rheo.close()