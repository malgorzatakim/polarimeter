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
    def __init__(self, capture_time, config):
        self.capture_time = capture_time
        self.config = config

    def acquire(self):
        """Aquires data for capture_time (seconds) via acquisition PC.
        Returns time, and signals of hannel A and channel B.
        """
        trigger_path = self.config["experiment_trigger_file"]

        with open(trigger_path,'w') as f:
            f.write("{}".format(self.capture_time))

        while True:
            with open(trigger_path,'r') as f:
                if f.read() is "0":
                    break
                time.sleep(0.1)

        self.last_data_timestamp = str(int(time.time()))
        filepath_old = self.config["experiment_raw_data_file"]
        filepath_new = os.path.join(self.config["experiment_raw_data_destination_folder"] + self.last_data_timestamp + ".csv")
        shutil.move(filepath_old, filepath_new)

        return np.loadtxt(filepath_new, delimiter=',', dtype=np.dtype('d'), unpack=True)

    def lastDataTimestamp(self):
        return self.last_data_timestamp

class SimulatedDataAcquirer(IDataAcquirer):
    def __init__(self, time=1, phase_difference=14, samplingrate=16384, amp_A=1, amp_B=1):
        """
        capture_time (s)
        phase_difference (degrees)
        samplingrate (Hz)
        """
        self.time = time
        self.phase_difference = phase_difference
        self.samplingrate = samplingrate
        self.amp_A = amp_A
        self.amp_B = amp_B

    def acquire(self):
        t = np.arange(0, self.time, 1 / self.samplingrate)
        f = 10
        # Random initial phase for chA
        phiA = random() * 2 * np.pi
        sigA = self.amp_A * np.cos(2 * np.pi * f * t + phiA) ** 2
        sigA += np.random.rand(len(sigA)) * 0.01 * self.amp_A

        # Add the phase difference for chB
        phiB = phiA - (self.phase_difference * np.pi / 180)
        sigB = self.amp_B * np.cos(2 * np.pi * f * t + phiB) ** 2
        sigB += np.random.rand(len(sigB)) * 0.01 * self.amp_B
        return t, sigA, sigB

    def lastDataTimestamp(self):
        return str(int(time.time()))

class RecordedDataAcquirer(IDataAcquirer):
    def __init__(self, folder_path):
        self.folder_path = folder_path
        all_filenames = os.listdir(folder_path)
        filtered_filenames = [file for file in all_filenames if file.endswith(".csv")]
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
