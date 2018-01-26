import os
import multiprocessing
# 宣告產生的新 process 要執行的函數與參數, 利用 os.getpid() 可以得知目前 process id
def worker(number):
    print('[{}][{}] handle number : {}'.format(os.getpid(),
                                               multiprocessing.current_process().name,
                                               number))
# Process 的產生有幾種作法, Unix 上預設 fork, Windows 上 預設 spawn.
# 在 Windows 上以 __name__ == '__main__' 隔離生成 process 的程式碼,
# 避免在 child process 發生無止盡重複產生 process.
if __name__ == '__main__':
    jobs = []
    print('[{}] Creating workers ...'.format(os.getpid()))
    for i in range(3):
        # 建立 Process, 並指定要執行的函數與參數
        p = multiprocessing.Process(target=worker, name='Worker {}'.format(i), args=(i,))
        jobs.append(p)
        p.start()