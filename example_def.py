import os
def create_and_write_to_file(*args):
    # args 是一個 tuple, 長度由呼叫者所傳入的參數數量而定
    # 注意 - 錯誤處理
    """
    if args is None and len(arg) < 1:
        print('Error : File cannot be created !')
        return
    """
    file_path = args[0]
    lyrics = args[1]
    handle = open(file_path, 'w')
    handle.write(lyrics)
    handle.close()

def file_path_builder(folder, file_name):
    return os.path.join(folder, file_name)

def get_file_data(file_path, lines = False):
    handle = open(file_path, 'r')
    data = None
    # 利用 if / elif / else 作條件對應的動作
    if lines:
        data = handle.readlines()
    else:
        data = handle.read()
    return data

def main():
    cwd = os.getcwd()
    name = 'example_def.txt'
    file_path = file_path_builder(cwd, name)

    lyrics_w = '我被擊敗了 你是擊敗人\n對你的期望太高 玩弄了我太傷人\n' +\
               '又被擊敗了 你是最超然的擊敗人\n' +\
               '我才剛剛交出真心 你卻扣繳我的真誠\n' +\
               '淚流某個海洋裡翻騰\n' +\
               '你是最巨大的擊敗人\n' +\
               '你是擊敗人'

    create_and_write_to_file(file_path, lyrics_w)

    lyrics_r = get_file_data(file_path)
    # lyrics_r = get_file_data(file_path, True)
    # lyrics_r = get_file_data(file_path, lines=True)
    print(lyrics_r)

main()