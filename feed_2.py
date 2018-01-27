
import os
f = open('/home/kilikkuo/Projects/py/py3_101/new_lyrics.txt', 'w')
line1st = 'It\'s late in the evening\n'
line2nd = 'She\'s wondering what clothes to wear\n'
line3rd = 'She puts on her make-up'
line4th = ' and brushes her long blond hair'
# 寫入
f.write(line1st)
f.write(line2nd)
f.write(line3rd)
f.write(line4th)
# 關閉檔案
f.close()
