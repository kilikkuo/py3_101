import threading

# 宣告帶有參數的函數, 並且此參數印出
def worker(number):
    print('I\'m working and I got number {}'.format(number))

threads = []
for i in range(3):
    # 建立執行緒, 並指定執行函數, 以及該函數所需要的參數 tuple
    t = threading.Thread(target=worker, args=(i,))
    threads.append(t)
    t.start()
