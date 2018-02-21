from labview import acquire
from polarimeter import Polarimeter

p = Polarimeter(source=acquire, sourceargs={'capture_time': 1, })
p.measure()

print('{} +/- {} at {}'.format(p.phase_difference, p.stdeviation, p.last_measured))


# import os


# def pretty_print_result(timestamp, phase_difference):
#     line = '{:s}, {:07.3f} degrees'
#     print(line.format(time.asctime(time.gmtime(timestamp)),
#                       phase_difference))


# def run(output_file=None, duration=30, units='s', print_output=True,
#         log_signals=False):
#     """Repeatedly run measurements for specified duration.

#     Returns mean and std of phase differences, and number of measurements.

#     Parameters
#     ----------
#     output_file : str, optional
#         Filename where to save timestamp and phase difference.
#     duration : int
#         Time to repeat measurements for
#     units: str
#         's'(econds), 'm'(inutes), 'h'(ours) or 'd'(ays).
#     print_output: bool
#         If true, print time and phase difference; default: True.
#     log_signals: bool
#         Save raw signal data; default: False.

#     Example
#     -------
#     run('foo.txt', duration=3, units='s')

#     """

#     if output_file is None:
#         output_file = 'temp.txt'

#     # Convert time into seconds
#     if units == 's': # seconds
#         pass
#     elif units == 'm': # minutes
#         duration *= 60
#     elif units == 'h': # hours
#         duration *= 60 * 60
#     elif units == 'd': # days
#         duration *= 24 * 60 * 60
#     else:
#         raise ValueError(('Unit must be seconds (s), minutes (m), hours (h)'
#                           ' or days (d).'))

#     start = time.time()

#     # repeatedly acquire data
#     while time.time() < start + duration:
#         t, phi = measure(save_data=log_signals)
#         write_result(output_file, t, phi)

#         if print_output:
#             pretty_print_result(t, phi)

#     # load all the data to compute stats
#     t, phi  = np.loadtxt(output_file, delimiter=',', unpack=True)

#     if output_file is 'temp.txt':
#         os.remove('temp.txt')

#     return np.mean(phi), np.std(phi, ddof=1), len(phi)

# def write_result(filename, timestamp, phase_difference):
#     """Append to filename the timestamp and phase difference.
#     Returns line that was written as a string.
#     """
#     f = open(filename, 'a')
#     string = '{}, {:.15f}\n'.format(timestamp, phase_difference)
#     f.write(string)
#     f.close()
#     return string