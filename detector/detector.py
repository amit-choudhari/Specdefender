import numpy as np
import pandas as pd
import pickle

from Counter import Counter

import threading
import subprocess
import sys, getopt
import time

class Detector:
    def __init__ (self, name, pid, trained_model):
        self.counter = Counter(name,pid)
        self.model = pickle.load(open(trained_model, 'rb'))

    def _preprocess(self, data_attack):
        c = 'perf'
        data_new = data_attack.set_index([data_attack.groupby(c).cumcount() + 1, c]).unstack().sort_index(1, 1)
        data_new.columns = data_new.columns.droplevel(0)
        #data_new['y'] = np.ones([data_new.shape[0],1])

        # remove outliers
        for df in data_new:
            q_low = data_new[df].quantile(0.01)
            q_hi  = data_new[df].quantile(0.99)
            data_new = data_new[(data_new[df]< q_hi) & (data_new[df] > q_low)]
        
        # create 3 new features branch miss rate, cache miss rate, spec load
        data_new['br_miss_rate']=data_new['armv8_cortex_a72/br_mis_pred/'].truediv(data_new['armv8_cortex_a72/br_pred/'])
        data_new['cache_miss_rate']=data_new['cache-misses'].mul(100).truediv(data_new['cache-references'])
        data_new['spec_load'] = data_new['ldst_spec'].truediv(data_new['ldst_spec'].max())
        
        X_test = data_new[['cache_miss_rate','spec_load']]
        return X_test

    def _detect(self, X_test):
        # Predict
        loaded_model = self.model
        preds = loaded_model.predict(X_test)
        spectre_prob = preds.mean()
        if spectre_prob > 0.70:
            print ("Spectre detected!!", spectre_prob*100,"%")
        else:
            print ("safe execution..", 100-spectre_prob*100,"%")

    def _start_detector(self, data):
        t = threading.currentThread()
        processed_data = self._preprocess(data)
        result = self._detect(processed_data)

    def start(self, timeout):
        poll_time = timeout
        while True:
            self.counter.run(poll_time)
            data = self.counter.get_data()
            #self.counter.clear_data()
            t = threading.Thread(target=self._start_detector, args=(data,))
            t.start()
            t.join()
            time.sleep(2) 

        print('exit start()')
        return 0

    def stop(self):
        pass


def main(argv):
    trained_model = 'finalized_model.sav'
    data_file = '../data/data.csv'
    timeout = 20
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

    print("pid:",pid,"timeout",timeout,"sec")
    detector = Detector(data_file, pid, trained_model)
    result = detector.start(timeout)
    if result == True:
        print("Spectre detected!")
        print("TODO Patch code")

    detector.stop()

main(sys.argv[1:])
