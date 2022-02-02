import pandas as pd

import os
import sys
import subprocess
import threading
import ctypes
import time

class Counter:
    def __init__ (self, name, pid):
        threading.Thread.__init__(self)
        self.filename = name+'.csv'
        self.pid = pid

    def _start_counter(self,arg):
        count = 0
        proc = subprocess.Popen(["perf stat -x ', ' -e armv8_cortex_a72/br_mis_pred/,armv8_cortex_a72/br_pred/,cache-misses,cache-references,ldst_spec -I 10 -a"],timeout=3)
        time.sleep(2) 
        proc.terminate()
        proc = subprocess.Popen(["pkill -f perf"],shell =True)
        proc.terminate()
        #while(True):
        #   time.sleep(2) 
        #   print(count)
        #   count = count+1

    def get_id(self):
        # returns id of the respective thread
        if hasattr(self, '_thread_id'):
            return self._thread_id
        for id, thread in threading._active.items():
            print("ID:",id)
        return id

    def _raise_exception(self, ident):
        thread_id = ident
        res = ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id,
              ctypes.py_object(SystemExit))
        print('killed')
        if res > 1:
            ctypes.pythonapi.PyThreadState_SetAsyncExc(thread_id, 0)
            print('Exception raise failure')

    # start counter thread
    def start(self, timeout):
        #t = threading.Thread(target=self._start_counter, args=("task",))
        #t.start()
        #time.sleep(timeout)
        print("killing self")
        #self._raise_exception(t.get_ident())

    #stop counter thread
    def stop(self):
        pass

    # read file and return array
    def get_data(self):
        pass

    # clear file
    def clear_data(self):
        pass
