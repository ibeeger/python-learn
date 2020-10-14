import threading
import time



class TaskThread(threading.Thread):
    def __init__(self, func, args=()):
        super(TaskThread, self).__init__()
        self.func = func
        self.args = args

    def run(self):
        self.result = self.func(self.args)

    def getresult(self):
        try:
            return self.result
        except Exception as ex:
            print(ex)
            return "ERROR"

