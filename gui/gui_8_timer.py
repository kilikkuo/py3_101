import matplotlib.pyplot as plt
import numpy as np
import random
import threading

fig, ax = plt.subplots()
# 透過 numpy 的 linespace 來建立一個 array [-3, -2, -1, 0, 1, 2, 3]
x = np.linspace(-3, 3)
# x = [-3, -2, -1, 0, 1, 2, 3]
# 設定 axes 的軸刻度
ax.axis([-3, 3, 0, 9])

# 建立一個 count 變數來計次
count = 0
def update_title(axes):
    # 每一次 timer 時間到, 將 count 次數加 1
    # 每 30 次就將 axes 清空, 並重設軸刻度
    global count
    count += 1
    if count % 30 == 0:
        count = 0
        axes.clear()
        ax.axis([-3,3,0,9]) # min_x, max_x, min_y, max_y 
    # 畫出新的曲線, 並且透過 figure.canvas.draw 把圖 render 出來.
    axes.plot(x, x*x*random.random())
    axes.figure.canvas.draw()

stop_call = False
def call_update_title_loop(t, axes):
    global stop_call
    import time
    while not stop_call:
        # 睡 t 秒之後醒來呼叫 update_title
        time.sleep(t)
        update_title(axes)

# 宣告 timer 變數, 等等用來儲存真正的物件
timer = None
# 用來指定是否使用 threading 模組的 timer
use_threading_timer = False
if use_threading_timer:
    timer = threading.Timer(0, call_update_title_loop, args=(0.1, ax))
else:
    # 建立一個 timer 物件, 每 100 ms 呼叫一次 callback, 預設是 1000 ms
    timer = fig.canvas.new_timer(interval=100)
    # 告物 timer callback 函數為何, 並且給予對應參數
    timer.add_callback(update_title, ax)

assert timer is not None, '應該要有 Timer 物件'
# 啟動 timer
timer.start()

plt.show()

if use_threading_timer:
    # 將 stop_call 設成 True, 以便讓 timer thread 的 while loop 被中斷
    stop_call = True
    timer.join()