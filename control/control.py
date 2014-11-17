import serial
import argparse
import logging
from time import sleep

class Controller():
	def __init__(self, port):
		"""Create Controller object.

		Controller to switch the laser and gimbal motor on and off.
		"""
		self.connection = serial.Serial(port, 9600, timeout=10)
		self.laserPower = None
		self.gimbalPower = None
		sleep(1)

		logging.info('Controller object created')

	def laser(self, power=True):
		"""Switch laser on and off."""

		if power:
			self.connection.write('L') # laser on
		else:
			self.connection.write('l') # laser off

		if self.connection.read(1) != '1':
			raise ControllerError('No response to laser command')
		else:
			self.laserPower = power

		logging.info('Laser power: %s', str(self.laserPower))
		return self.laserPower

	def gimbal(self, power=True):
		"""Switch gimbal on and off."""

		if power:
			self.connection.write('G') # gimbal on
		else:
			self.connection.write('g') # gimbal off

		if self.connection.read(1) != '1':
			raise ControllerError('No response to gimbal command')
		else:
			self.gimbalPower = power

		logging.info('Gimbal power: %s', str(self.gimbalPower))
		return self.gimbalPower

	def __str__(self):
		return 'Laser: %s\nGimbal: %s' % (str(self.laserPower), 
										  str(self.gimbalPower))

class ControllerError(Exception):
	pass

if __name__ == '__main__':
	parser = argparse.ArgumentParser(description='Command line interface to '
									 'control laser and gimbal motor.')
	parser.add_argument('-s', '--serial', default='/dev/ttyACM0', help='Serial'
						' port for controller. Default is /dev/ttyACM0.')

	laser_group = parser.add_mutually_exclusive_group()

	laser_group.add_argument('-lon', '--laseron', dest='laser', default=None,
							 action='store_true', help='Turn laser on')
	laser_group.add_argument('-loff', '--laseroff', dest='laser', default=None,
							 action='store_false', help='Turn laser off')

	gimbal_group = parser.add_mutually_exclusive_group()
	gimbal_group.add_argument('-goff', '--gimbaloff', dest='gimbal',
							  action='store_false',	help='Turn gimbal off',
							  default=None)
	gimbal_group.add_argument('-gon', '--gimbalon', dest='gimbal',
							  action='store_true', help='Turn gimbal on',
							  default=None)

	args = parser.parse_args()

	c = Controller(args.serial)

	if args.laser is not None:
		c.laser(power=args.laser)
	
	if args.gimbal is not None:
		c.gimbal(power=args.gimbal)
	
	print c