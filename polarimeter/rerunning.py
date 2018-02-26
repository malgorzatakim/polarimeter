from polarimeter import Polarimeter
from data_acquirers import RecordedDataAcquirer

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