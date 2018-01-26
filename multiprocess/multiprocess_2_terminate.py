import time
import multiprocessing
def worker():
    print('Starting ...')
    time.sleep(5)
    # Exiting 將不會被印出, 因為程序被強制中止
    print('Exiting ...')
if __name__ == '__main__':
    p = multiprocessing.Process(target=worker)
    print('[{}] BEFORE - {}'.format(p, p.is_alive()))
    p.start()
    print('[{}] DURING - {}'.format(p, p.is_alive()))

    time.sleep(1)

    p.terminate()
    print('[{}] TERMINATED - {}'.format(p, p.is_alive()))
    # 呼叫 join 來讓程序後端有足夠時間更新與此 p process 有關之狀態
    p.join()
    print('[{}] JOINED - {}'.format(p, p.is_alive()))