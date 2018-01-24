import threading

# 透過 threading 模組提供的 currentThread() 可以得到目前運行的執行緒本體
# 透過執行緒本體的 getName() 可以得到該執行緒被指定的名字
def welding():
   print('I\'m {}'.format(threading.currentThread().getName()))
def casting():
   print('I\'m {}'.format(threading.currentThread().getName()))

# 建立執行緒, 並且指定名稱
t1 = threading.Thread(name='Bob', target=welding)
t2 = threading.Thread(name='John', target=casting)
t1.start()
t2.start()