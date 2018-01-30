import matplotlib.pyplot as plt
import matplotlib.image as mpimg

img_data = mpimg.imread('helloworld.jpg')
plt.title(' Hello World ! ')
plt.imshow(img_data)
# 標示 X 軸在[100, 200, 500, 1000] 的位置
plt.xticks([100, 200, 500, 1000])
plt.show()