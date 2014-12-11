from __future__ import division
import bitlib as bl
import argparse
import logging
import os

def main(capture_time, repeat=1):
    """Acquire data from channels A and B for capture_time (seconds)
    with the specified number of repeat measurements. Automatically uses
    the highest sample rate possible. Note that the actual capture time
    may be slightly different to that requested (check t[-1]).

    Returns:
        t: time for each sample (seconds)
        chA: list of lists containing signal (volts) from channel A at
        times in t.
        chB: as above but for channel B.

    If there are n repeats, len(chA) and len(chB) == n.

    Example:
        t, chA, chB = main(10)

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
            while len(chA) < repeat:
                # BitScope configuration
                while True:
                    try:
                        assert bl.BL_Select(bl.BL_SELECT_DEVICE,0) == 0
                        assert bl.BL_Mode(bl.BL_MODE_DUAL) == 1 # capture mode

                        for channel in [0, 1]:
                            assert bl.BL_Select(bl.BL_SELECT_CHANNEL, channel) == channel
                            assert bl.BL_Select(bl.BL_SELECT_SOURCE, bl.BL_SOURCE_POD) == 0
                            assert bl.BL_Range(2) == 3.5
                            assert bl.BL_Offset(-1.75) == -1.75
                            assert bl.BL_Enable(True) == True

                        bl.BL_Rate(bl.BL_MAX_RATE)
                        bl.BL_Size(bl.BL_MAX_SIZE)
                        bl.BL_Time(capture_time)
                        actual_rate = bl.BL_Rate(bl.BL_ASK)
                        actual_size = bl.BL_Size(bl.BL_ASK)
                    except:
                        logging.warning('Assertion error during BitScope config. '
                                        'Re-trying...')
                        continue
                    break

                # Measurement and data acquisition
                bl.BL_Trace()

                channel = 0
                assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
                chA.append(bl.BL_Acquire())

                channel = 1
                assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
                chB.append(bl.BL_Acquire())
        finally:
            bl.BL_Close()
            os.chdir(intial_dir)
    else:
        raise Exception('Unable to open connection to BitScope')

    time = [t / actual_rate for t in range(0, actual_size)]
    return time, chA, chB

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Acquire data with BitScope on'
                                     ' channels A and B and print to stdout.')
    parser.add_argument('time', help='capture time (seconds)', type=float)
    parser.add_argument('-header', help='print header row', action='store_true')
    args = parser.parse_args()

    if args.header:
        print 'time (s), chA (V), chB (V)'

    time, chA, chB = main(args.time)

    for t, chA, chB in zip(time, chA[0], chB[0]):
        print '%f,%f,%f' % (t, chA, chB)
