import os
# 取得目前工作目錄
cwd = os.getcwd()
# 組合欲寫入的檔案名稱
f = open(os.path.join(cwd, 'new_lyrics.txt'), 'w', encoding='utf8')

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
