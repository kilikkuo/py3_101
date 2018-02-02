from matplotlib import pyplot as plt

class LineBuilder(object):
    def __init__(self, line):
        self.line = line
        # 把 line2D 物件裡面的所有點的 x 和 y 值取出各自產生一個 list
        self.xs = list(line.get_xdata())
        self.ys = list(line.get_ydata())
        # 連接在 figure 上接收到的 mouse press/release event 給指定的函數
        self.cid_down = line.figure.canvas.mpl_connect('button_press_event', self.on_pressed)
        self.cid_up = line.figure.canvas.mpl_connect('button_release_event', self.on_released)

    def __add_new_line(self, x, y):
        print('Add new line >>>> ')
        self.xs.append(x)
        self.ys.append(y)
        # 將含有所有點的 x,y 座標串列透過 set_data 函數交給 Line2D 物件繪圖
        self.line.set_data(self.xs, self.ys)
        self.line.figure.canvas.draw()

    def on_pressed(self, event):
        print('on_pressed : {}'.format(event))
        # 確定 event 所在的 axes 與 劃線所在的 axes 是一樣的, 不然就不處理該 event
        if event.inaxes != self.line.axes:
            return
        # 如果 press 的座標跟上一條線的最後一點座標一樣, 就不需要新增線段.
        if self.xs[-1] != event.xdata or self.ys[-1] != event.ydata:
            self.__add_new_line(event.xdata, event.ydata)
        pass

    def on_released(self, event):
        print('on_released : {}'.format(event))
        # 確定 event 所在的 axes 與 劃線所在的 axes 是一樣的, 不然就不處理該 event
        if event.inaxes != self.line.axes:
            return
        # 如果 release 的座標跟 press 下去的點座標一樣, 就不需要新增線段.
        if self.xs[-1] != event.xdata or self.ys[-1] != event.ydata:
            self.__add_new_line(event.xdata, event.ydata)

    def get_connected_cids(self):
        return [self.cid_down, self.cid_up]

fig, ax = plt.subplots()
ax.set_title('Click on axes to build line segments')
# 在(0, 0)處畫一個, 因為 plot 回傳一個 Line2D 物件, 所以只有一個點並不會出現一條線.
line, = ax.plot([0], [0])
# 將此 Line2D 物件傳給 LineBuilder
lb = LineBuilder(line)

plt.show()

# 將與 figure 連結的 cid 斷開連結
for id in lb.get_connected_cids():
    fig.canvas.mpl_disconnect(id)