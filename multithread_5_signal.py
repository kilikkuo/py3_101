import threading
import time

def wait_for_event(e):
    print('[block] wait_for_event starting')
    # 此執行緒會在此等待, 一直到 e 的狀態被 set 為止
    event_is_set = e.wait()
    print('[block] event set: {}'.format(event_is_set))

def wait_for_event_with_timeout(e, t):
    # 此執行緒會進行迴圈, 檢查如果 e 的狀態沒有被 set, 就進入執行
    while not e.isSet():
        print('[block-with-timeout] wait_for_event_with_timeout starting')
        # 在此等待 t 秒, 並取得 e 的設定狀態
        event_is_set = e.wait(t)
        print('[block-with-timeout] event set: {}'.format(event_is_set))
        if event_is_set:
            print('[block-with-timeout] processing event')
        else:
            print('[block-with-timeout] doing other work')

# 建立一個 Event 物件, 並傳給 t1, t2 兩條執行緒
evt = threading.Event()
# 指定執行緒 t1 的執行函數為 wait_for_event
t1 = threading.Thread(name='block',
                      target=wait_for_event,
                      args=(evt,))
# 指定執行緒 t1 的執行函數為 wait_for_event_with_timeout
t2 = threading.Thread(name='block-with-timeout',
                      target=wait_for_event_with_timeout,
                      args=(evt, 2))
t1.start()
t2.start()

# t1, t2 啟動後, 讓主執行緒睡眠 3 秒後設定 evt 物件.
time_to_sleep = 3
print('[Main] Waiting {} seconds before calling Event.set()'.format(time_to_sleep))
time.sleep(time_to_sleep)
evt.set()
print('[Main] Event is set')