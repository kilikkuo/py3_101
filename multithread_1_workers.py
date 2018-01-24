 # 匯入 threading module
import threading

# 宣告一個函數給執行緒來執行
def worker():
    print('I\'m working')
# 宣告一個 list 來存放產生出來的執行緒
threads = []
# 建立三個執行緒, 並且都指定 worker 作為他們的執行函數,
# 建立完後並啟動這些執行緒
for i in range(3):
    t = threading.Thread(target=worker)
    threads.append(t)
    t.start()