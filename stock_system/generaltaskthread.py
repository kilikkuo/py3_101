from threading import Thread, Event, Lock, current_thread
from logger import *

# 執行任務的基本單位
class Task(Logger):
    __id = 0
    def __init__(self, *args, **argd):
        Logger.__init__(self)
        Task.__id += 1
        self.__taskid = Task.__id

    # 覆寫 __getattr__, 只允許取得指定名稱的 attr 的值
    def __getattr__(self, name):
        if name == "taskid":
            return self.__taskid
        return None

    # 尚未實作, 留給繼承的子類實作
    def run(self):
        raise NotImplementedError

    # 取得目前任務執行所在的執行緒名
    def get_current_thread_name(self):
        t = current_thread()
        return t.name

class TaskThread(Thread):
    def __init__(self, name = "Unknown"):
        Thread.__init__(self, name = name)
        # 用來保護此 TaskThread 的內容操作
        self.__qlock = Lock()

        self.tasks = []
        self.wati_for_task = Event()
        self.wati_for_stop = Event()
        # 設 True 將會印出 debug message
        self.debug = False

    def debug_log(self, msg, prefixname = False, postfixname = False):
        if self.debug:
            self.log(msg, prefixname, postfixname)

    def log(self, msg, prefixname = False, postfixname = False):
        pre = "[%s]"%(self.name) if prefixname else ""
        post = "[%s]"%(self.name) if postfixname else ""
        print(pre+msg+post)

    def start(self):
        # 啟動 TaskThread
        Thread.start(self)

    def run(self):
        self.log(">>>>> TT : start running ...", prefixname = True)
        while True:
            # 如果沒有等待被執行的 task, 則利用 event 的 wait 機制避免執行緒一直在迴圈忙碌
            if len(self.tasks) == 0:
                self.wati_for_task.wait()

            # 如果 stop() 被呼叫了, 迴圈將會在這個條件處中斷, 剩餘的 task 都不會被執行.
            if self.wati_for_stop.isSet():
                break

            # 從 tasks 串列中取出一個等待被執行的 task, 必須使用 lock 保護以防止此處取出
            # task 的同時, 有其他執行緒正在進行 addtask / canceltask 等動作
            self.__qlock.acquire()
            task = self.tasks.pop(0)
            self.__qlock.release()

            if task:
                # 執行任務
                self.debug_log(">>>>> TT : start executing ... task (%d)"%(task.taskid), prefixname = True)
                task.run()
        self.log(">>>>> TT : ending.", prefixname = True)

    def stop(self):
        self.log("stop ...", postfixname = True)
        self.wati_for_stop.set()
        self.wati_for_task.set()
        self.join()
        self.tasks.clear()
        self.tasks = None
        self.wati_for_task = None
        self.wati_for_stop = None
        self.__qlock = None

    def addtask(self, task):
        self.debug_log("adding task(%d) to ..."%(task.taskid), postfixname = True)
        # 新增一個 task
        self.__qlock.acquire()
        self.tasks.append(task)
        self.__qlock.release()
        self.wati_for_task.set()
        self.wati_for_task.clear()
        return task.taskid

    def canceltask(self, taskid):
        self.debug_log("canceling task(%d) in ..."%(taskid), postfixname = True)
        self.__qlock.acquire()
        # 取消一個尚未被執行的任務, taskid 必須相符合
        task = list(filter(lambda x: x.taskid == taskid, self.tasks))
        if len(task) == 1:
            self.tasks.remove(task[0])
            self.debug_log("task(%d) canceled in ..."%(taskid), postfixname = True)
        self.__qlock.release()
