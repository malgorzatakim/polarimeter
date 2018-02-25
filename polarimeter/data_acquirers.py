from __future__ import division
from random import random
import abc
import numpy as np
import os
import shutil
import time


class IDataAcquirer(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def acquire(self):
        raise NotImplementedError("Method acquire() must be implemeted.")

    @abc.abstractmethod
    def lastDataTimestamp(self):
        raise NotImplementedError("Method lastDataTimestamp() must be implemeted.")

class RealDataAcquirer(IDataAcquirer):
    def __init__(self, capture_time):
        self.capture_time = capture_time

    def acquire(self):
        """Aquires data for capture_time (seconds) via acquisition PC.
        Returns time, and signals of hannel A and channel B.
        """
        trigger_path = 'C:\\Users\\jdmgroup\\Desktop\\trigger.txt'

        with open(trigger_path,'w') as f:
            f.write("{}".format(self.capture_time))

        while True:
            with open(trigger_path,'r') as f:
                if f.read() is "0":
                    break
                time.sleep(0.1)

        self.last_data_timestamp = str(int(time.time()))
        filepath_old = "C:\\polarimeter\\trace.csv"
        filepath_new = os.path.join("C:\\polarimeter\\results_trace\\" + self.last_data_timestamp + ".csv")
        shutil.move(filepath_old, filepath_new)

        #filepath_new = "/Users/maglorzatanguyen/Documents/IMPERIAL/Year_4/pol_combinations/trace_ref_7feb.csv"
        return np.loadtxt(filepath_new, delimiter=',', dtype=np.dtype('d'), unpack=True)

    def lastDataTimestamp(self):
        return self.last_data_timestamp

class SimulatedDataAcquirer(IDataAcquirer):
    def __init__(self, time=1, phase_difference=14, samplingrate=16384):
        """
        capture_time (s)
        phase_difference (degrees)
        samplingrate (Hz)
        """
        self.time = time
        self.phase_difference = phase_difference
        self.samplingrate = samplingrate

    def acquire(self):
        t = np.arange(0, self.time, 1 / self.samplingrate)
        f = 10
        A = 1
        # Random initial phase for chA
        phiA = random() * 2 * np.pi
        sigA = A * np.cos(2 * np.pi * f * t + phiA) ** 2
        sigA += np.random.rand(len(sigA)) * 0.01 * A

        # Add the phase difference for chB
        phiB = phiA - (self.phase_difference * np.pi / 180)
        sigB = A * np.cos(2 * np.pi * f * t + phiB) ** 2
        sigB += np.random.rand(len(sigB)) * 0.01 * A
        return t, sigA, sigB

    def lastDataTimestamp(self):
        return str(int(time.time()))

class SimulatedDataAcquirerJ(IDataAcquirer):
    def __init__(self, time=0.3, samplingrate=16384):
        """
        capture_time (s)
        samplingrate (Hz)
        """
        self.time = time
        self.samplingrate = samplingrate

    def acquire(self):
        t = np.arange(0, self.time, 1 / self.samplingrate)
        f = 10
        A = 0.6
        B = 0.7
        T0 = 0.2
        # Random initial phase for chA
        phiA = 0
        sigA = A * np.cos(2 * np.pi * f * t + phiA) ** 2 + T0
        sigA += np.random.rand(len(sigA)) * 0.01

        # Add the phase difference for chB
        phiB = phiA - np.pi * (1/3)
        sigB = B * np.cos(2 * np.pi * f * t + phiB) ** 2 +T0
        sigB += np.random.rand(len(sigB)) * 0.01
        return t, sigA, sigB

    def lastDataTimestamp(self):
        str(int(time.time()))

class RecordedDataAcquirer(IDataAcquirer):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        all_filenames = os.listdir(folder_path)
        filtered_filenames = [file for file in all_filenames if file.endswith(".txt")]
        self.recorded_data_files = list(reversed(filtered_filenames))

    def acquire(self):
        data_file = self.recorded_data_files.pop()
        self.last_data_timestamp = data_file
        file_path = self.folder_path + data_file
        return np.loadtxt(file_path, delimiter=',', dtype=np.dtype('d'), unpack=True)

    def isDataAvailable(self):
        return len(self.recorded_data_files) > 0

    def lastDataTimestamp(self):
        return self.last_data_timestamp
