import time
import multiprocessing
def wait_for_event(e):
    print('[block] wait_for_event starting')
    # 此子程序會在此等待, 一直到 e 的狀態被 set 為止
    event_is_set = e.wait()
    print('[block] event set: {}'.format(event_is_set))

def wait_for_event_with_timeout(e, t):
    # 此子程序會進行迴圈, 檢查如果 e 的狀態沒有被 set, 就進入執行
    while not e.is_set():
        print('[block-with-timeout] wait_for_event_with_timeout starting')
        # 在此等待 t 秒, 並取得 e 的設定狀態
        event_is_set = e.wait(t)
        print('[block-with-timeout] event set: {}'.format(event_is_set))
        if event_is_set:
            print('[block-with-timeout] processing event')
        else:
            print('[block-with-timeout] doing other work')

if __name__ == '__main__':
    # 建立一個 Event 物件, 並傳給 p1, p2 兩個子程序
    evt = multiprocessing.Event()
    p1 = multiprocessing.Process(target=wait_for_event, args=(evt,))
    p2 = multiprocessing.Process(target=wait_for_event_with_timeout, args=(evt, 1))
    p1.start()
    p2.start()

    # p1, p2 啟動後, 讓主程序睡眠 3 秒後設定 evt 物件.
    time_to_sleep = 3
    print('[Main] Waiting {} seconds before calling Event.set()'.format(time_to_sleep))
    time.sleep(time_to_sleep)
    evt.set()
    print('[Main] Event is set')