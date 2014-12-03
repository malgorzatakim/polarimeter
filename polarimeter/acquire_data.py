from __future__ import division
import bitlib as bl
import argparse
import os

def main(samples, sample_rate):
    """Acquire specified number of samples at a specified sample rate on
     channels A and B."""

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

    """Now do trace parameters. bl.BL_Rate must always be specified
    and it should be the first parameter assigned when preparing a
    new trace. Note that if this sample rate can't be selected, the
    nearest sample rate will be returned."""
    try:
        actual_sample_rate = bl.BL_Rate(sample_rate)
        assert sample_rate == actual_sample_rate
    except AssertionError:
        raise AssertionError('Maximum sample rate of %i sps available. '
                             'Requested %i sps.' % (actual_sample_rate, 
                                                    sample_rate))

    """Next is number of samples. Returned value is actual number of
    samples returned."""
    try:
        actual_samples = bl.BL_Size(samples)
        assert samples == actual_samples
    except AssertionError:
        raise AssertionError('Maximum of %i samples available. Requested %i '
                             'samples.' % (actual_samples, samples))

    bl.BL_Trace()

    # get data from each channel
    channel = 0
    assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
    chA = bl.BL_Acquire()

    channel = 1
    assert bl.BL_Select(bl.BL_SELECT_CHANNEL,channel) == channel
    chB = bl.BL_Acquire()

    bl.BL_Close()

    time = [t / sample_rate for t in range(0, samples)]
    
    os.chdir(intial_dir)
    
    return time, chA, chB

if __name__ == '__main__':
    # defaults
    samples = 5000
    sample_rate = 10000
    
    parser = argparse.ArgumentParser(description='Acquire data with BitScope on'
                                     ' channels A and B and print to stdout.')
    parser.add_argument('-n', dest='samples',
                        help='number of samples to acquire (default %i)'
                        % samples, type=int)
    parser.add_argument('-r', dest='sample_rate', help='samples/second (default'
                        ' %i)' % sample_rate, type=int)
    parser.add_argument('-header', help='print header row', action='store_true')
    args = parser.parse_args()

    if args.samples:
        samples = args.samples

    if args.sample_rate:
        sample_rate = args.sample_rate

    if args.header:
        print 'time (s), chA (V), chB (V)'

    time, chA, chB = main(samples=samples, sample_rate=sample_rate)

    for t, chA, chB in zip(time, chA, chB):
        print '%f,%f,%f' % (t, chA, chB)
