from bitlib import *
import numpy as np
import argparse
import os

def main(samples,sample_rate):
    """Acquire specified number of samples at a specified sample rate on
     channels A and B."""

    """The BitScope library is stupid. It changes the working directory
    to whatever connection the BitScope is on and doesn't put it back
    afterwards. Makes importing this as a module a nightmare, because
    you try to reload the module and the Python interpreter can't find
    it. Get the current working directory, store it, then change back to
    the directory at the end. Terrible."""
    intial_dir = os.getcwd()

    assert BL_Open() == 1 # returns number devices opened

    """First, must select device. Returns index of selected entity.
    Note that it is 0-indexed."""
    assert BL_Select(BL_SELECT_DEVICE,0) == 0

    """Second, select the capture mode. This must happen after
    selecting the device but before selecting channels."""
    BL_Mode(BL_MODE_DUAL) # prefered capture mode

    """Now select each channel in turn and configure. Returns index
    of selected channel if channel has been successfully
    selected."""
    channels = [0,1]
    for channel in channels:
        assert BL_Select(BL_SELECT_CHANNEL,channel) == channel

        # not sure if this should be bnc
        BL_Select(BL_SELECT_SOURCE,BL_SOURCE_POD)

        """Set the voltage range. Can get the number of ranges from
        BL_Count(BL_COUNT_RANGE). This returns 5. Can set the maxi
        range using BL_Range(BL_Count(BL_COUNT_RANGE) (11 V) but I
        only want 5 V. This is an index of 3. BL_Range returns max
        voltage. """
        assert BL_Range(3) == 5.2
        
        # Enable the channel
        assert BL_Enable(True) == True

    """Now do trace parameters. BL_Rate must always be specified
    and it should be the first parameter assigned when preparing a
    new trace. Note that if this sample rate can't be selected, the
    nearest sample rate will be returned."""
    try:
        actual_sample_rate = BL_Rate(sample_rate)
        assert sample_rate == actual_sample_rate
    except AssertionError:
        print('Maximum sample rate of %i sps available. Requested sample rate '
            'of %i sps.' % (actual_sample_rate, sample_rate))
        raise AssertionError

    """Next is number of samples. Returned value is actual number of
    samples returned."""
    try:
        actual_samples = BL_Size(samples)
        assert samples == actual_samples
    except AssertionError:
        print('Maximum of %i samples available. Requested %i samples'
              % (actual_samples, samples))
        raise AssertionError

    # do trace, acquire data
    BL_Trace()

    # get first channel
    channel = 0
    assert BL_Select(BL_SELECT_CHANNEL,channel) == channel
    chA = BL_Acquire()

    # get second channel
    channel = 1
    assert BL_Select(BL_SELECT_CHANNEL,channel) == channel
    chB = BL_Acquire()

    BL_Close()

    # provide times samples were taken
    time = np.arange(0,1.0*samples/sample_rate,1.0/sample_rate)
    
    # print output: time (s), chA (V), chB (V)
    for t, chA, chB in zip(time, chA, chB):
        print '%f,%f,%f' % (t, chA, chB)

    # change directory to where we were at the start
    os.chdir(intial_dir)

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

    main(samples=samples,sample_rate=sample_rate)
