import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec

fig = plt.figure()
# 調整 Figure 內的所有 subplot 的位置
fig.subplots_adjust(bottom=0.05, left=0.1, top = 0.95, right=0.9)
# 宣告一個 3x3 的 gridspec
gs = gridspec.GridSpec(3, 3)
# 第一個 Axes 所在的位置是 row index 為 0, 佔滿所有 column.
ax1 = plt.subplot(gs[0, :])
ax1.set(title='GridSpec')
# 第二個 Axes 所在的位置是 row index 為 1, 佔據的 column 為 [:-1].
ax2 = plt.subplot(gs[1,:-1])

# 第三個 Axes 所在的位置是 row index 為 1, 佔據的 column 為最後 1 個.
ax3 = plt.subplot(gs[1:, -1])
plt.xticks(()), plt.yticks(())
# 第四個 Axes 所在的位置是 row index 為 -1 (最後一個 row), 佔據的 column index 為 0
ax4 = plt.subplot(gs[-1,0])
plt.xticks(()), plt.yticks(())
# 第五個 Axes 所在的位置是 row index 為 -1 (最後一個 row), 佔據的 column 為倒數第二個.
ax5 = plt.subplot(gs[-1,-2])
plt.xticks(()), plt.yticks(())
# 在 Ax5 上寫入文字, 起始座標為 x=0.5, y=0.5 (照axes比例), 並且水平/垂直方向置中.
ax5.text(0.5, 0.5, 'Axes 5', ha='center', va='center', size=20, alpha=0.5)

# tight_layout 可以讓 subplot 盡可能的 fit 在設定好的 figure 內. 並讓
# text / titile / ticks 等內容可以呈現.
plt.tight_layout()
plt.show()
