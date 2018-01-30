import matplotlib.pyplot as plt
import matplotlib.markers as mkrs
import random

# https://matplotlib.org/api/markers_api.html
markers = ['p', '*', '+', 'x', 'd', 'o', 'v', 's', 'h', '<', '4']
# R/G/B 為各自隨機的 0 ~ 1 之間的數字.
colors = [(random.random(), random.random() / 3, random.random() / 2 ) for x in range(len(markers))]

# 準備 x, y 軸資料
x_items = [i for i in range(1, len(markers)+1)]
y_items = [random.randint(1, len(markers)) for i in range(len(markers))]

while len(markers) > 0:
    marker = markers.pop()
    color = colors.pop()
    x = x_items.pop()
    y = y_items.pop()
    # 一次只畫一個點, 帶入指定的顏色與標記
    plt.plot(x, y, color=color, marker=marker)

plt.ylabel('y')
plt.xlabel('x')
plt.grid(True)
plt.show()