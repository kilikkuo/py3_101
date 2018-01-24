import time
import random
import threading

# 一個計數器物件
class Counter(object):
    def __init__(self, start=0):
        self.lock = threading.Lock()
        # 給定一個起始值, 在物件生成時預設數值為 0
        self.value = start
    def increment(self, actor):
        print('[{}] Waiting for lock'.format(actor))
        self.lock.acquire()
        try:
            print('[{}] Acquired lock'.format(actor))
            # 將 value 的值增加 1, 用 lock 保護住避免產生 race condition
            self.value = self.value + 1
        finally:
            # 利用 try / except / final 的例外處理 pattern 來確保 lock 一定會在
            # 結束時釋放, 避免產生 dead lock.
            self.lock.release()

def worker(c):
    name = threading.currentThread().getName()
    # 隨機產生一個 [0.0, 1.0) 的小數浮點數, 並且讓 worker 睡著該秒數後在對 counter 物件
    # 進行加一.
    # 這個動作重複兩次.
    for i in range(2):
        pause = random.random()
        print('[{}] Sleeping {:.3f} seconds'.format(name, pause))
        time.sleep(pause)
        c.increment(name)
    print('[{}] Done'.format(name))

# 建立一個 Counter 物件, 並傳給 t1, t2
counter = Counter()
t1 = threading.Thread(name='Bob', target=worker, args=(counter,))
t2 = threading.Thread(name='John', target=worker, args=(counter,))
t1.start()
t2.start()

print('[Main] Waiting for worker threads')
main_thread = threading.currentThread()
# 在此程序的 main thread 中等待 t1, t2 結束, 才離開程序
for t in threading.enumerate():
    if t is not main_thread:
        t.join()
print('[Main] Counter: {}'.format(counter.value))