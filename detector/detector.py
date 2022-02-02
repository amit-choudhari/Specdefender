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

    def __preprocess():
        # Load the dataset
        fields = ['value', 'perf']
        data_attack = pd.read_csv(data_file, skipinitialspace=True, usecols=fields, sep = ", ", engine='python')
        #print(data_attack.head())
        
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

    def _detect():
        # Predict
        loaded_model = pickle.load(open(trained_model, 'rb'))
        preds = loaded_model.predict(X_test)
        spectre_prob = preds.mean()
        if spectre_prob > 0.70:
            print ("Spectre detected!!", spectre_prob*100,"%")
        else:
            print ("safe execution..", 100-spectre_prob*100,"%")

    def _start_detector(self, poll_timeout):
        print(poll_timeout)
        t = threading.currentThread()
        while getattr(t, "do_run", True):
            self.counter.start(poll_timeout)
            self.counter.get_data()
            self.counter.clear_data()
            self.counter.stop()
        self.counter.stop()

    def start(self, timeout):
        poll_time = 5
        proc = subprocess.Popen(["perf stat -x ', ' -e armv8_cortex_a72/br_mis_pred/,armv8_cortex_a72/br_pred/,cache-misses,cache-references,ldst_spec -I 10 -a"], shell=True)
        time.sleep(2) 
        proc.terminate()
        #t = threading.Thread(target=self._start_detector, args=(poll_time,))
        #t.start()
        #counter.stop()

        #time.sleep(timeout)
        #t.do_run = False
        print('exit start()')
        return 0

    def stop(self):
        pass


def main(argv):
    trained_model = 'finalized_model.sav'
    #data_file = '../data/data.csv'
    data_file = '../data/normal.csv'
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
