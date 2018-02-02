import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button, RadioButtons

fig, ax = plt.subplots()
plt.suptitle('Figure Title')
plt.subplots_adjust(left=0.25, bottom=0.25)

t = np.arange(0.0, 10.0, 0.1)
s = t*1
l, = plt.plot(t, s, lw=2, color='red')
ax.axis([0, 10, 0, 100])

axcolor = 'lightgoldenrodyellow'
axslope = plt.axes([0.25, 0.1, 0.65, 0.03], facecolor=axcolor)
sslope = Slider(axslope, 'Slope', 0, 10.0, valinit=1)
def update(val):
    pass
    new_slope = val
    l.set_ydata(new_slope*t)
    fig.canvas.draw_idle()
sslope.on_changed(update)

# 以上為 gui_6_slider.py 的程式碼
# 設定一個新的 Axes 區域給重置按鈕(Reset Button), 並指定滑鼠移動到上面的時候顏色變淡
resetax = plt.axes([0.8, 0.025, 0.1, 0.04])
button = Button(resetax, 'Reset', color=axcolor, hovercolor='0.975')
# 實做 Reset Button 按下去之後發生的邏輯
def reset(event):
    l.set_ydata(1*t)
    fig.canvas.draw_idle()
# Button 利用 on_clicked 來掛載回調函數
button.on_clicked(reset)
# 建立一個新的 Axes 留給 Radio Button, 並宣告 Radio Button 有三個選項,
# 'red', 'blue', 'green', 而且起始狀態為 index 0(也就是紅色)
rax = plt.axes([0.025, 0.5, 0.15, 0.15], facecolor=axcolor)
radio = RadioButtons(rax, ('red', 'blue', 'green'), active=0)
def colorfunc(label):
    l.set_color(label)
    fig.canvas.draw_idle()
# Radio Button 利用 on_clicked 來掛載回調函數
radio.on_clicked(colorfunc)
fig.savefig('button.png')
plt.show()