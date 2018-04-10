from argparse import ArgumentParser

from data_acquirers import RealDataAcquirer, SimulatedDataAcquirer, RecordedDataAcquirer
from polarimeter import Polarimeter
import time
import os
import numpy as np

class Runner():
    def experiment(self):
        capture_time = 1
        acquirer = RealDataAcquirer(capture_time)
        p = Polarimeter()
        phase_diff, stdev = p.measure(*acquirer.acquire())

        print('{} +/- {} at {}'.format(phase_diff, stdev, acquirer.lastDataTimestamp()))

    def exper_time(self):
        capture_time = 1
        acquirer = RealDataAcquirer(capture_time)
        p = Polarimeter()
        x = 5 # how many flushes to file
        y = 10 # experiment count per one flush
        timestamp = int(time.time())
        #results_file = os.path.join("/Users/maglorzatanguyen/Desktop/results/" + str(timestamp) + ".txt")
        results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")

        with open(results_file, "w") as f:
            for _ in range(x):
                for _ in range(y):
                    data = acquirer.acquire()
                    phase_diff, stdev = p.measure(*data)
                    f.write("{},{},{}\n".format(acquirer.lastDataTimestamp(), phase_diff, stdev))
                #time.sleep(300)
                f.flush()

    def exper_time2(self):
        phase_difference = 60
        acquirer = SimulatedDataAcquirer(phase_difference=phase_difference)
        p = Polarimeter()

        x = 6 # how many flushes to file, no of data points
        y = 10 # experiments taken into mean
        timestamp = int(time.time())
        results_file = os.path.join("/Users/maglorzatanguyen/Desktop/results/" + str(timestamp) + ".txt")
        #results_file = os.path.join("C:\\polarimeter\\results\\" + str(timestamp) + ".txt")
        #### build string from 3 parts: path to file (basic name), timestamp, ".txt"

        with open(results_file, "w") as f:
            for _ in range(x):
                t = int(time.time())
                data = []
                for _ in range(y):
                    phase_diff, stdev = p.measure(*acquirer.acquire())
                    data.append([acquirer.lastDataTimestamp(), phase_diff, stdev])
                phase = []
                stdev = []
                for i in range(len(data)):
                    phase.append(data[i][1])
                    stdev.append(data[i][2])
                f.write("{},{},{}\n".format(t, np.mean(phase), np.mean(stdev)))
                f.flush()

    def rerunning(self):
        results_file = "C:\\polarimeter\\results_trace_rerunning\\results\\result_rerunning.txt"
        #results_file = "/Users/malgorzatanguyen/Desktop/rerun.txt"
        with open(results_file, 'w') as f:
            data_folder_path = "C:\\polarimeter\\results_trace_rerunning\\"
            #data_folder_path = "/Users/malgorzatanguyen/Desktop/results_trace1/"
            acquirer = RecordedDataAcquirer(data_folder_path)
            p = Polarimeter()
            while acquirer.isDataAvailable():
                data = acquirer.acquire()
                phase_diff, stdev = p.measure(*data)
                f.write("{},{},{}\n".format(acquirer.lastDataTimestamp(), phase_diff, stdev))

    def laser_stability(self):
        x = 7000 #how many flushes to file
        y = 10 #no of experiments in a single flush
        timestamp = int(time.time())
        results_file = os.path.join(
            "C:\\polarimeter\\results\\" + str(timestamp) + "_stab.txt")

        with open(results_file, "w") as f:
            for _ in range(x):
                for _ in range(y):
                    times = int(time.time())
                    acquirer = RealDataAcquirer(1)
                    one_acq = acquirer.acquire()
                    chA = one_acq[:,1]
                    chB = one_acq[:,2]
                    final_chA = np.mean(chA)
                    final_chB = np.mean(chB)
                    f.write("{},{},{}\n".format(times, final_chA, final_chB))
            f.flush()

def main():
    parser = ArgumentParser()
    parser.add_argument("scenario", nargs=1)
    args = parser.parse_args()
    scenario = args.scenario[0]
    if scenario == 'experiment':
        Runner().experiment()
    elif scenario == 'exper_time':
        Runner().exper_time()
    elif scenario == 'exper_time2':
        Runner().exper_time2()
    elif scenario == 'laser_stability':
        Runner().laser_stability()
    elif scenario == 'rerunning':
        Runner().rerunning()
    else:
        raise Exception("Uknown scenario: {}".format(args.scenario))

if __name__ == "__main__":
    main()
