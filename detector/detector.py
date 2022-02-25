import numpy as np
import pandas as pd
import pickle

from Counter import Counter
from patch import Patch

import threading
import subprocess
import sys, getopt
import time
import psutil

class Detector:
    def __init__ (self, name, pid, trained_model):
        self.counter = Counter(name,pid)
        self.pid = pid
        self.model = pickle.load(open(trained_model, 'rb'))
        self.spectre = False

    def _preprocess(self, data_attack):
        c = 'perf'
        data_new = data_attack.set_index([data_attack.groupby(c).cumcount() + 1, c]).unstack().sort_index(1, 1)
        data_new.columns = data_new.columns.droplevel(0)
        #data_new['y'] = np.ones([data_new.shape[0],1])
        data_new = data_new.replace('<not counted>', np.nan).dropna()

        if data_new.size <5:
            return False

        # remove outliers
        for df in data_new:
            q_low = data_new[df].quantile(0.01)
            q_hi  = data_new[df].quantile(0.99)
            data_new = data_new[(data_new[df]< q_hi) & (data_new[df] > q_low)]
        
        # create 3 new features branch miss rate, cache miss rate, spec load
        data_new['br_miss_rate']=data_new['armv8_cortex_a72/br_mis_pred/'].truediv(data_new['armv8_cortex_a72/br_pred/'])
        data_new['cache_miss_rate']=data_new['cache-misses'].mul(100).truediv(data_new['cache-references'])
        data_new['spec_load'] = data_new['ldst_spec'].truediv(data_new['ldst_spec'].max())
        
        self.X_test = data_new[['cache_miss_rate','spec_load']]
        return True

    def _detect(self):
        # Predict
        loaded_model = self.model
        preds = loaded_model.predict(self.X_test)
        spectre_prob = preds.mean()
        if spectre_prob > 0.70:
            print ("Spectre detected!!", spectre_prob*100,"%")
            self.spectre = True;
        else:
            self.spectre = False;
            print ("safe execution..", 100-spectre_prob*100,"%")

    def _start_detector(self, data):
        t = threading.currentThread()
        if self._preprocess(data) == False:
            self.spectre = False
            return
        result = self._detect()

    def getResult(self):
        return self.spectre

    def start(self, timeout):
        poll_time = timeout
        #while True:
        ret = self.counter.run(poll_time)
        if ret == False:
            return
        data = self.counter.get_data()
        #self.counter.clear_data()
        t = threading.Thread(target=self._start_detector, args=(data,))
        t.start()
        t.join()
        #time.sleep(2) 

        print('exit start()')
        return 0

    def stop(self):
        pass


def main(argv):
    trained_model = 'finalized_model.sav'
    data_file = '../data/data.csv'
    timeout = 2
    '''
    try:
        opts, args = getopt.getopt(argv,"ht:p:",["timeout=","pid="])
    except getopt.GetoptError:
        print('detector.py -t <timeout(sec)> -p <processid>')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-t", "--timeout"):
            timeout = int(arg)
        elif opt in ("-p", "--pid"):
            pid = int(arg)
        else:
            print('detector.py -i <inputfile> -o <outputfile>')
            sys.exit()
    '''

    for proc in psutil.process_iter():
        pid = proc.pid
        #pid = 1436
        #pid = 5421
        if pid < 5000:
            continue
        print("==================")
        print("pid:",pid,"timeout",timeout,"sec")
        detector = Detector(data_file, pid, trained_model)
        detector.start(timeout)
        if detector.getResult() == True:
            print("Spectre detected!")
            safe_proc = Patch(pid)
            safe_proc.runPatchedProc()
            print("Patched!!")
            print("TODO Patch code")
        else:
            print("No Spectre :)")
        print("")

    detector.stop()

#main(sys.argv[1:])
main(sys.argv[0:])
