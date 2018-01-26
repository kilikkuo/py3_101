import os
# from queue import Empty
from multiprocessing import Process, Queue

def get_and_put(q):
    q.put([10, 'hi', None])
    print('[{}] {}'.format(os.getpid(), q.get()))
    # try:
    #     print('[{}] {}'.format(os.getpid(), q.get(True, 1)))
    # except Empty:
    #     print('[{}] get nothing !'.format(os.getpid()))
    #     pass

if __name__ == '__main__':
    q = Queue()
    p = Process(target=get_and_put, args=(q,))
    p.start()
    print('[{}] {}'.format(os.getpid(), q.get()))
    # import time
    # time.sleep(2)
    q.put(['gg'])
    p.join()
