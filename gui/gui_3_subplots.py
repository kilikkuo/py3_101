import matplotlib.pyplot as plt
import math

# 準備要被畫出來的資料
# x 為 0 ~ 1, 每隔 0.01 為一單位
# y 為 x 值乘上 pi
a1x = [i/100 for i in range(0 * 100, 1 * 100)]
a1y = [math.sin(math.pi * i) for i in a1x]

a2x = [i/100 for i in range(0 * 100, 2 * 100)]
a2y = [1 + math.cos(math.pi * i * 2) for i in a2x]

# 透過 subplots() 可以快速得到一個 figure 與一個 axes
# 也可以透過指定 subplots() 參數得到對應的 n x m 個 axes, (row, col, index)
# 得到的 axes list 順序 => 左上到右下.
fig, ax = plt.subplots(2,1)
print('Lenth of ax : {}'.format(len(ax)))
ax[0].plot(a1x, a1y)
ax[0].set(ylabel='y value 0', title='Simple Figure & Multi Axes')
ax[0].grid()

ax[1].set(xlabel='x value ', ylabel='y value 1')
ax[1].plot(a2x, a2y)

fig.savefig('gui_3.png')
plt.show()