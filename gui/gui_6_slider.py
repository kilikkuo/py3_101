import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

# 宣告一個 axes 區域要將資料/函數繪出, 並設定其起始範圍從左邊 1/4 起,
# 從底部 1/4 起.
fig, ax = plt.subplots(facecolor='red')
plt.suptitle('Figure Title')
plt.subplots_adjust(left=0.25, bottom=0.25)

# 宣告一個 numpy array t, 數值從 0 ~ 10, 元素單位間隔 0.1
# [0, 0.1, 0.2, 0.3, ..., 10.0]
t = np.arange(0.0, 10.0, 0.1)
# 宣告另一個 array s, 其內元素為 所有的 t 元素乘上 1.
s = t*1
# 將 t, s 畫出來, 線寬 2, 紅色.
# pyplot.plot 回傳的是一個 list, 包含了連續的線圖.
l, = plt.plot(t, s, lw=2, color='red')
# 設定 ax 的兩個軸項單位為多少, x 軸 0 ~ 10, y 軸 0 ~ 100.
ax.axis([0, 10, 0, 100])

# 設定顏色
# 想知道所有有名字的顏色
# for name, hex in matplotlib.colors.cnames.items():
#     print(name, hex)
axcolor = 'lightgoldenrodyellow'
# 透過 plot.axes 即可建立一個新的 Axes, 並指定其位置在整張 figure 的這個
# [0.25(左), 0.1(下), 0.65(寬), 0.03(高)] 區域, 並將 Slider 物件指定給
# 這個 Axes. Slider 名字是 'Slope', 最小值 0, 最大值 10.0, 初始值 1.
axslope = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
sslope = Slider(axslope, 'Slope', 0, 10.0, valinit=1)

# update 為每次 Slider 收到滑鼠拖曳變動後, 執行的回調函數.
# 需定義一參數 val 為更新後的值, 將更新後的值重新計算並修改畫出來的Line2D物件.
def update(val):
    pass
    new_slope = val
    l.set_ydata(new_slope*t)
    # 在計算完成後, 若程式處於 idle 狀態才執行繪圖更新, 避免過度忙碌浪費資源.
    fig.canvas.draw_idle()
# on_change 是 Slider 用來掛載回調函數的函數.
sslope.on_changed(update)
# 顯示 grid
ax.grid(True)
plt.show()