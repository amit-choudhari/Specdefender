import subprocess
from subprocess import Popen, PIPE
import threading
import ctypes
import time
import psutil

class Patch:
    def __init__ (self, pid):
        self.pid = pid

    def _getPatchedBin(self):
        # load the file from known location
        cmd = "readlink -f /proc/"+str(self.pid)+"/exe"
        pipe = subprocess.Popen([cmd], stdout=PIPE, shell=True)
        self.path = pipe.communicate()[0]
        self.path = self.path.decode() 
        self.path = self.path.strip('\n')
        print(self.path);
        pass

    def runPatchedProc(self):
        # execute the file in constrained env
        self._getPatchedBin()
        cmd = "kill -9 "+str(self.pid)
        pipe = subprocess.Popen([cmd], stdout=PIPE, shell=True)
        cmd = self.path+'_safe -m 20 -l 100 -t 100 2>&1 | tee output' 
        print(cmd)
        self.proc = subprocess.Popen([cmd], shell = True)
        print(self.proc.pid)
        pass

    def stopPatchedFile(self):
        # stop once the attack is disappeared
        self.proc.kill()
        pass

    def runSafeProc(self):
        # execute the file in constrained env
        self._getPatchedBin()
        cmd = "kill -9 "+str(self.pid)
        pipe = subprocess.Popen([cmd], stdout=PIPE, shell=True)
        cmd = '/home/kali/amit/Specdefender/test'+'/safe 2>&1 | tee output' 
        print(cmd)
        self.proc = subprocess.Popen([cmd], shell = True)
        print(self.proc.pid)
        pass

    def runNormalProc(self):
        # execute the file in constrained env
        self._getPatchedBin()
        cmd = "kill -9 "+str(self.pid)
        pipe = subprocess.Popen([cmd], stdout=PIPE, shell=True)
        cmd = '/home/kali/amit/Specdefender/test'+'/normal 2>&1 | tee output' 
        print(cmd)
        self.proc = subprocess.Popen([cmd], shell = True)
        print(self.proc.pid)
        pass
