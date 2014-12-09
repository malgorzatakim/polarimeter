from __future__ import division
import bitlib as bl
import argparse
import os

def main(capture_time, repeat=1):
    """Acquire data from channels A and B for capture_time (seconds)
    with the specified number of repeat measurements. Automatically uses
    the highest sample rate possible. Note that the actual capture time
    may be slightly different to that requested (check t[-1]).

    Returns:
        t: time for each sample (seconds)
        chA: signal (volts) from channel A
        chB: signal (volts) from channel B

    chA and chB are lists of lists containing repeat measurements.

    Example:
        t, chA, chB = main(10)
    """

    """BitScope library changes working directory. Need to change back
    at the end of the function."""
    intial_dir = os.getcwd()

    assert bl.BL_Open() == 1 # returns number devices opened

    """First, must select device. Returns index of selected entity.
    Note that it is 0-indexed."""
    assert bl.BL_Select(bl.BL_SELECT_DEVICE,0) == 0

    """Second, select the capture mode. This must happen after
    selecting the device but before selecting channels."""
    bl.BL_Mode(bl.BL_MODE_DUAL) # prefered capture mode

    """Now select each channel in turn and configure. Returns index
    of selected channel if channel has been successfully
    selected."""
    channels = [0,1]
    for channel in channels:
        assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel

        # not sure if this should be bnc
        bl.BL_Select(bl.BL_SELECT_SOURCE,bl.BL_SOURCE_POD)

        """Set the voltage range. Can get the number of ranges from
        bl.BL_Count(bl.BL_COUNT_RANGE). This returns 5. Can set the max
        range using bl.BL_Range(bl.BL_Count(bl.BL_COUNT_RANGE) (11 V)
        but I only want 5 V. This is an index of 3. bl.BL_Range returns
        max voltage."""
        assert bl.BL_Range(3) == 5.2

        # Enable the channel
        assert bl.BL_Enable(True) == True

        # Set rate/size
        bl.BL_Rate(bl.BL_MAX_RATE)
        bl.BL_Size(bl.BL_MAX_SIZE)
        actual_time = bl.BL_Time(capture_time)
        actual_rate = bl.BL_Rate(bl.BL_ASK)
        actual_size = bl.BL_Size(bl.BL_ASK)

    def do_measurement():
        bl.BL_Trace()

        channel = 0
        assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
        chA = bl.BL_Acquire()

        channel = 1
        assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
        chB = bl.BL_Acquire()

        return chA, chB

    if repeat == 1:
        chA, chB = do_measurement()
    else:
        chA = list()
        chB = list()

        for i in range(repeat):
            a, b = do_measurement()
            chA.append(a)
            chB.append(b)

    bl.BL_Close()

    time = [t / actual_rate for t in range(0, actual_size)]
    
    os.chdir(intial_dir)
    
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

    for t, chA, chB in zip(time, chA, chB):
        print '%f,%f,%f' % (t, chA, chB)
