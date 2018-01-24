import threading
import time
# daemon 執行緒要執行的函式
def daemon():
    print('[{}] Starting'.format(threading.currentThread().getName()))
    time.sleep(2)
    print('[{}] Exiting'.format(threading.currentThread().getName()))

# 建立一條名為 daemon 的執行緒, 並指定為 daemon
d = threading.Thread(name='daemon', target=daemon)
d.setDaemon(True)

def non_daemon():
    print('[{}] Starting'.format(threading.currentThread().getName()))
    print('[{}] Exiting'.format(threading.currentThread().getName()))

t = threading.Thread(name='non-daemon', target=non_daemon)

d.start()
t.start()

# 使用 join() 函數, 來讓 main thread 等待直到 daemon thread 完成工作
d.join()
t.join()
