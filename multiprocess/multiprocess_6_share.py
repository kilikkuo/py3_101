from multiprocessing import Process, Value, Array
def compute(val, arr):
    print('[Child] 執行計算中 ... ')
    val.value = 3.14
    for idx, item in enumerate(arr):
        arr[idx] = item * 2
if __name__ == '__main__':
    val = Value('d', 0.0)
    arr = Array('i', range(5))
    print('[Parent] 初始化 Value : {} / Array : {}'.format(val.value, arr[:]))
    p = Process(target=compute, args=(val, arr))
    p.start()
    p.join()
    print('[Parent] Value : {} / Array : {}'.format(val.value, arr[:]))