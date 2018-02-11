import os
def create_and_write_to_file(*args):
    # args 是一個 tuple, 長度由呼叫者所傳入的參數數量而定
    # 注意 - 錯誤處理, 如果傳進來的參數 args 數量與下方程式碼之存取不符, 會有 exception
    """
    if args is None and len(arg) < 1:
        print('Error : File cannot be created !')
        return
    """
    file_path = args[0]
    lyrics = args[1]
    handle = open(file_path, 'w', encoding='utf8')
    # 將資料寫入
    handle.write(lyrics)
    # 結束寫入, 關閉檔案
    handle.close()

def file_path_builder(folder, file_name):
    return os.path.join(folder, file_name)

def get_file_data(file_path, lines = False):
    handle = open(file_path, 'r', encoding='utf8')
    data = None
    # 利用 if / elif / else 作條件對應的動作
    if lines:
        print(' >>> readlines ... ')
        data = handle.readlines()
    else:
        print(' >>> read ... ')
        data = handle.read()
    return data

def main():
    cwd = os.getcwd()
    name = 'example_def.txt'
    # 將程式執行所在目錄與要產生的檔案名稱組合成一個完整路徑
    file_path = file_path_builder(cwd, name)

    lyrics_w = '我被擊敗了 你是擊敗人\n對你的期望太高 玩弄了我太傷人\n' +\
               '又被擊敗了 你是最超然的擊敗人\n' +\
               '我才剛剛交出真心 你卻扣繳我的真誠\n' +\
               '淚流某個海洋裡翻騰\n' +\
               '你是最巨大的擊敗人\n' +\
               '你是擊敗人'

    create_and_write_to_file(file_path, lyrics_w)

    lyrics_r = get_file_data(file_path)
    print(lyrics_r)
    # readlines 會將換行符號 '\n' 當成字元一起讀入, 需要處理
    lyrics_r = get_file_data(file_path, True)
    print(lyrics_r)
    # lyrics_r = get_file_data(file_path, lines=True)

main()