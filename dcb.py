from __future__ import print_function 
import pumpy.pumpy as pumpy
import rheodyne.rheodyne as rheodyne
import autosampler.autosampler as autosampler
import math
import sys
import argparse
import logging

logging.basicConfig(level=logging.INFO)

# Units used throughout
# length: mm
# volume: uL (mm^3)
# time: minutes

# Set up the command line argument parser
parser = argparse.ArgumentParser(description='dcb reactor')
parser.add_argument('-p',dest='primed',help='Indicates additives already primed',action="store_true")
args = parser.parse_args()

# Injection loop volume
il_vol = int(math.pi * (1.0/2)**2 * 1000)

# Create chain object for syringe pumps 
chain = pumpy.Chain('COM1')

# Create syringe objects and configure pumps
# addpull: withdraws additive from selector and into IL
addpull = pumpy.Pump(chain,1,name='add pull')
addpull.setdiameter(12.06) # BD Plastipak 5 mL

# addpush: injects into IL to push additive out
addpush = pumpy.Pump(chain,2,name='add push')
addpush.setdiameter(19.13) # BD Plastipak 20 mL
addpush.setflowrate(500)

# subcat: injects substrate and catalyst
subcat = pumpy.PHD2000(chain,3,name='subcat')
subcat.setdiameter(19.13) # BD Plastipak 20 mL
subcat.setflowrate(500)
subcat.settargetvolume(il_vol)

# Configure Arduino Rheodyne selector/six-port valve controller
rheo = rheodyne.Rheodyne('COM7')

# Configure Arduino autosampler
sampler = autosampler.Autosampler('COM3')

# Selector rinse
waste = 10 # waste position
waste_vol = 250 # volume to expell

# Additives in selector positions
additives = [1,2]

# Priming procedure. Use -p flag to skip.
if not args.primed:
	# Volume of tubing connecting the selector valve and additive reservoirs
	prime_vol = math.pi * (0.8/2.0)**2 * 650 # uL

	# Going to withdraw prime_vol * number of additives into injection loop
	# Make sure that the injection loop can accommodate this
	if prime_vol * len(additives) > il_vol:
		logging.critical('Injection loop can\'t accomodate',len(additives),'*',prime_vol,' uL for priming')
		sys.exit()
	else:
		logging.info('Begin priming procedure')
		
		rheo.valve(True) # 6-port load

		for additive in additives:
			logging.info('Priming additive %s of %s',additive,len(additives))

			# Prime additive
			rheo.selector(additive)
			addpull.settargetvolume(prime_vol * 1.2) # deliberately overfill
			addpull.withdraw()
			addpull.waituntiltarget()

			# Expel that volume from IL
			rheo.selector(waste)
			addpull.settargetvolume(prime_vol * 1.4) # deliberately even more
			addpull.infuse()
			addpull.waituntiltarget()

		logging.info('Priming procedure complete')

# Next inject additives one by one

addpull.settargetvolume(il_vol)
addpush.settargetvolume(il_vol*1.2) # deliberately expell more

rf = 1000 # flow rate of substrate, additive and catalysts.
subcat.setflowrate(rf)
addpush.setflowrate(rf)

for additive in additives:
	logging.info('Additive %s of %s',additive,len(additives))
	
	# Load into IL
 	rheo.valve(True) # 6-port load
 	rheo.selector(additive) # selector to additive
 	addpull.setflowrate(500)
 	addpull.withdraw()
 	addpull.waituntiltarget()

 	# Rinse selector
 	rheo.selector(waste)
 	addpull.setflowrate(rf)
 	addpull.infuse()
 	# N.B. no waituntiltarget() because the next step will take longer

	# Inject IL
 	rheo.valve(False) # 6-port inject
 	addpush.infuse()
 	subcat.infuse()
 	addpush.waituntiltarget()

 	sampler.advance()

rheo.close()
chain.close()