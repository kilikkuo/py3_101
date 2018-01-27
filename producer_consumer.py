import threading
import multiprocessing
import time
import random
import queue
import os

# Set True : 雙程序模式的 Producer / Consumer
# Set False : 雙執行緒模式的 Producer / Consumer
process_mode = True

superClass = multiprocessing.Process if process_mode else threading.Thread
superQueue = multiprocessing.Queue if process_mode else queue.Queue
superEvent = multiprocessing.Event if process_mode else threading.Event
# 如果是程序模式, 印出 process id;如果是執行緒模式, 印出 thread identifier.
myid = os.getpid if process_mode else threading.get_ident

class Producer(superClass):
    def __init__(self, q, evt):
        super().__init__()
        self.q = q
        self.evt = evt

    def run(self):
        while not self.evt.is_set():
            if not self.q.full():
                item = random.randint(1,10)
                self.q.put(item)
                print('[Producer][{}] Putting {} in queue, now size : {}'.format(
                      myid(), item, self.q.qsize()))
            time.sleep(random.random())
        return

class Consumer(superClass):
    def __init__(self, q, evt):
        super().__init__()
        self.q = q
        self.evt = evt

    def run(self):
        while not self.evt.is_set():
            if not self.q.empty():
                item = self.q.get()
                print('[Consumer][{}] Getting {} from queue, now size : {}'.format(
                      myid(), item, self.q.qsize()))
            time.sleep(random.random())
        return

if __name__ == '__main__':
    q = superQueue(10)
    evt = superEvent()
    p = Producer(q, evt)
    c = Consumer(q, evt)

    p.start()
    c.start()
    time.sleep(10)
    evt.set()
    print('[Main] bye')
