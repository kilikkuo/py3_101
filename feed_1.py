# 匯入 “os” 這個 module, 藉此使用包含在內的函式
import os
cwd = os.getcwd()
print('目前工作目錄 : {}'.format(cwd))

# 列出目前路徑目錄下的所有東西
print('工作目錄下有 : {}'.format(os.listdir(cwd)))

file_path = os.path.join(cwd, 'JayChou_lyric.txt')

# (檔案路徑, 開啟模式, 編碼方式), 因為內文有中文, 在 Windows 中文作業系統
# 上會預設用 cp950 當作編碼方式, 會導致 python 讀取中文檔案遇到例外
# 試試把 encoding 拿掉.
file_handle = open(file_path, 'r', encoding = 'utf8')

# 資料讀入記憶體
file_data = file_handle.read()
print('data read : {} '.format(file_data))

# 將檔案指標指回開頭
file_handle.seek(0)
# readlines 會將換行符號 '\n' 一起當成字元讀入, 需額外處理
file_data_lines = file_handle.readlines()
print('data readlines: {} '.format(file_data_lines))

print('------------------')
# 將串列裡的 str 一行一行印出來 !
for i in file_data_lines:
    print(i)
