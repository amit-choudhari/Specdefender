import pandas as pd

import subprocess
import threading
import ctypes
import time
import psutil

class Counter:
    def __init__ (self, name, pid):
        threading.Thread.__init__(self)
        self.filename = name
        self.pid = pid

    def line_prepender(self, filename, line):
        with open(filename, 'r+') as f:
            content = f.read()
            f.seek(0, 0)
            f.write(line.rstrip('\r\n') + '\n' + content)

    # start counter thread
    def run(self, timeout):
        command = "perf stat -x ', ' -e armv8_cortex_a72/br_mis_pred/,armv8_cortex_a72/br_pred/,cache-misses,cache-references,ldst_spec -I 100 -p "+ str(self.pid) + " 2>&1 | tee " + self.filename
        print(command)
        proc = subprocess.Popen([command], shell = True)
        time.sleep(timeout)
        for proc in psutil.process_iter():
            # check whether the process name matches
            if any(procstr in proc.name() for procstr in\
                ['perf']):
                print(f'Killing {proc.name()}')
                proc.kill()
        cols ='value, empty, perf, temp1, temp2, temp3' 
        self.line_prepender(self.filename, cols)

    # read file and return array
    def get_data(self):
        # Load the dataset
        fields = ['value', 'perf']
        data = pd.read_csv(self.filename, skipinitialspace=True, usecols=fields, sep = ", ", engine='python')
        return data
        pass

    # clear file
    def clear_data(self):
        pass
