import pumpy.pumpy as pumpy
import rheodyne.rheodyne as rheodyne
import autosampler.autosampler as autosampler
import math

# Variables
IL_length = 100 # mm
IL_ID = 1 # mm
IL_vol = math.pi * (IL_ID/2.0)**2 * IL_length # uL
waste = 10 # waste position on selector
waste_rinse_vol = 100 # uL
fr_carrier = 100 # uL/min
fr_substrate = 100 # uL/min

# Configure autosampler
sampler = autosampler.Autosampler('COM3')

# Configure Arduino Rheodyne selector/six-port valve controller
rheo = rheodyne.Rheodyne('COM7')

# Configure pump chain
chain = pumpy.Chain('COM1')

# Configure additive withdrawer - withdraws from selector and into IL
pull = pumpy.Pump(chain,1) # 
pull.setdiameter(14.5)
pull.setflowrate(500)

# Configure additive pusher - pushes additive out of IL into reactor
push = pumpy.Pump(chain,2) 
push.setdiameter(14.5)
push.setflowrate(500)

# Configure carrier fluid
carrier = pumpy.Pump(chain,3)
carrier.setdiameter(15)
carrier.setflowrate(fr_carrier)

# Configure substrate and catalyst (same pump, PHD2000)
subcat = pumpy.PHD2000(chain,4)
subcat.setdiameter(15)
subcat.setflowrate(fr_substrate)

# Tests
for pump in [pull, push, carrier, subcat]:
    pump.infuse()

sampler.valve(True)
sampler.advance()
rheo.valve(True)
rheo.selector(2)
rheo.valve(False)
rheo.selector(7)
sampler.valve(False)

for pump in [pull, push, carrier, subcat]:
    pump.stop()