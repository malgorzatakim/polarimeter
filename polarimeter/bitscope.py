from __future__ import division
import bitlib as bl
import logging
import os

def acquire(rate=5000, size=5000, repeat=1):
    """Acquire data from channels A and B for with specified sample
    rate, capture size and number of repeat measurements.

    Returns:
        t: time for each sample (seconds)
        chA: list of lists containing signal (volts) from channel A at
        times in t.
        chB: as above but for channel B.

    If there are n repeats, len(chA) and len(chB) == n.

    Example:
        t, chA, chB = main(5000, 6000,3)

        where:
        t = [0.0001, 0.0002, ...]
        chA[0] = [voltage1, voltage2, ...]
        chB[0] = [voltage1, voltage2, ...]
    """

    """BitScope library changes working directory. Need to change back
    at the end of the function."""
    intial_dir = os.getcwd()

    chA = []
    chB = []

    if bl.BL_Open():
        try:
            # BitScope configuration
            while True:
                try:
                    assert bl.BL_Select(bl.BL_SELECT_DEVICE,0) == 0
                    assert bl.BL_Mode(bl.BL_MODE_DUAL) == 1 # capture mode

                    for channel in [0, 1]:
                        assert bl.BL_Select(bl.BL_SELECT_CHANNEL, channel) == channel
                        assert bl.BL_Select(bl.BL_SELECT_SOURCE, bl.BL_SOURCE_POD) == 0
                        assert bl.BL_Range(2) == 3.5
                        assert bl.BL_Offset(-1.65) == -1.65
                        assert bl.BL_Enable(True) == True

                    actual_rate = bl.BL_Rate(rate)
                    if actual_rate != rate:
                        logging.warning('Actual sampling rate (%.2f Hz) different'
                                        ' to requested sampling rate (%.2f Hz).'
                                        % (actual_rate, rate))

                    actual_size = bl.BL_Size(size)
                    if actual_size != size:
                        logging.warning('Actual capture size (%i samples) '
                                        'different to requested capture size '
                                        '(%i samples).' % (actual_size, size))
                except:
                    logging.warning('Assertion error during BitScope config. '
                                    'Re-trying...')
                    continue
                break

            # Measurement and data acquisition
            while len(chA) < repeat:
                trace = bl.BL_Trace(actual_rate*actual_size*10)
                state = bl.BL_State()
                if trace and (state == 2):
                    channel = 0
                    assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
                    chA.append(bl.BL_Acquire())

                    channel = 1
                    assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
                    chB.append(bl.BL_Acquire())
                else:
                    raise Exception('Trace error.\rTrace status %s with state %s' % (trace, state))
        finally:
            bl.BL_Close()
            os.chdir(intial_dir)
    else:
        raise Exception('Unable to open connection to BitScope')

    time = [t / actual_rate for t in range(0, actual_size)]
    return time, chA, chB