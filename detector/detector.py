import numpy as np
import pandas as pd
import pickle
import sklearn.model_selection as model_selection
import xgboost as xgb
from xgboost.sklearn import XGBClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.multiclass import OneVsRestClassifier

from Counter import Counter
from patch import Patch

import threading
import subprocess
import sys, getopt
import time
import psutil

ATTACK = 0
NORMAL = 1
SAFE_ATTACK = 2
SAFE = 3

class Detector:
    def __init__ (self, name, pid, trained_model):
        self.counter = Counter(name,pid)
        self.pid = pid
        self.model = pickle.load(open(trained_model, 'rb'))
        self.state = NORMAL

    def _preprocess(self, data_attack):
        c = 'perf'
        data_new = data_attack.set_index([data_attack.groupby(c).cumcount() + 1, c]).unstack().sort_index(1, 1)
        data_new.columns = data_new.columns.droplevel(0)
        #data_new['y'] = np.ones([data_new.shape[0],1])
        data_new = data_new.replace('<not counted>', np.nan).dropna()

        if data_new.size <5:
            return False

        #print(data_new)
        # remove outliers
        for df in data_new:
            q_low = data_new[df].quantile(0.01)
            q_hi  = data_new[df].quantile(0.99)
            data_new = data_new[(data_new[df]< q_hi) & (data_new[df] > q_low)]
        
        # create 3 new features branch miss rate, cache miss rate, spec load
        data_new['cache_miss_rate']=data_new['cache-misses'].mul(100).truediv(data_new['cache-references'])
        
        self.X_test = data_new[['cache_miss_rate','ldst_spec']]
        #print(self.X_test)
        return True

    def _detect(self):
        # Predict
        loaded_model = self.model
        preds = loaded_model.predict(self.X_test)
        print(preds)
        #spectre_prob = preds.mean()
        counts = np.bincount(preds.astype(int))
        print("####",np.argmax(counts))
        self.state = np.argmax(counts)
        if self.state == ATTACK:
            print ("[Normal]: Spectre detected!!")
            print ("[Normal]: Load spectre safe program!!")
            safe_proc = Patch(self.pid)
            safe_proc.runPatchedProc()
        elif self.state == NORMAL:
            print ("[Normal] execution!")
        elif self.state == SAFE_ATTACK:
            print ("[SAFE]: Spectre active!!")
            safe_proc = Patch(self.pid)
            safe_proc.runSafeProc()
        elif self.state == SAFE:
            print ("[SAFE]: safe execution..")
            print ("[SAFE]: Load normal program for better perf")
            safe_proc = Patch(self.pid)
            safe_proc.runNormalProc()

    def _start_detector(self, data):
        t = threading.currentThread()
        if self._preprocess(data) == False:
            self.spectre = False
            return
        self._detect()

    def getResult(self):
        return self.state

    def start(self, timeout):
        poll_time = timeout
        #while True:
        ret = self.counter.run(poll_time)
        if ret == False:
            return
        data = self.counter.get_data()
        t = threading.Thread(target=self._start_detector, args=(data,))
        t.start()
        t.join()
        #time.sleep(2) 
        print('exit start()')

    def stop(self):
        pass


def main(argv):
    trained_model = 'finalized_model_multi_class_ovo.sav'
    data_file = '../data/data.csv'
    timeout = 2

    while True:
        for proc in psutil.process_iter():
            pid = proc.pid
            if pid < 4565:
                continue
            print("==================")
            print("pid:",pid,"timeout",timeout,"sec")
            detector = Detector(data_file, pid, trained_model)
            detector.start(timeout)
            print("")
    #detector.stop()

#main(sys.argv[1:])
main(sys.argv[0:])
