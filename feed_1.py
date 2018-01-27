# 匯入 “os” 這個 module, 藉此使用包含在內的函式
import os
cwd = os.getcwd()
print('目前工作目錄 : {}'.format(cwd))

# 列出目前路徑目錄下的所有東西
print('工作目錄下有 : {}'.format(os.listdir(cwd)))

file_path = os.path.join(cwd, 'JayChou_lyric.txt')

# (檔案路徑, 開啟模式)
file_handle = open(file_path, 'r')

# 資料讀入記憶體
file_data = file_handle.read()
print('data read : {} '.format(file_data))

# 將檔案指標指回開頭
file_handle.seek(0)
file_data_lines = file_handle.readlines()
print('data readlines: {} '.format(file_data_lines))

