import matplotlib.pyplot as plt
# 準備要被畫出來的資料
x = [1,2,3,4,5]
y = [2,2,3,3,4]

# 透過 subplots() 可以快速得到一個 figure 與一個 axes
# 也可以透過指定 subplots() 參數得到對應的 n x m 個 axes, (row, col, index)
# 得到的 axes list 順序 => 左上到右下.
fig, ax = plt.subplots()
ax.plot(x, y)

# 需要在 show 之前先把圖檔儲存起來, 因為 show 之後 plt 進入解構狀態, fig 將無法正確儲存
fig.savefig("simple.png")
plt.show()
