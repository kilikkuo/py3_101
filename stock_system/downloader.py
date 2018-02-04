import re
import os, sys, csv, datetime
import time
import shutil
import traceback
import requests
from pprint import pprint

def crawl_tse_data_and_save(downloadDir, day, month, year):
    date_str = '{0}{1:02d}{2:02d}'.format(year, month, day)
    # 台灣證券交易所所有股價交易資料的 base url.
    url = 'http://www.twse.com.tw/exchangeReport/MI_INDEX'

    # 組合查詢參數, 查詢日期,回傳格式與查詢內容
    query_params = {
        'date': date_str,
        'response': 'json',
        'type': 'ALLBUT0999',
        '_': str(round(time.time() * 1000) - 500)
    }

    # 透過 requests 模組, 將欲查詢的 url 與 參數組傳入
    page = requests.get(url, params=query_params)

    # 如果上述的網路請求回傳的狀態值不為 ok, 則請求失敗.
    if not page.ok:
        print('[Status Error] Can not get TSE data on {}'.format(date_str))
        return False

    # 如果請求成功, 則將 page 內容裡的資料拿出放入 content.
    content = None
    try:
        content = page.json()
    except:
        traceback.print_exc()
        return False

    # 將資料格式重新整理, 網頁上的資料順序排法與實際上你想儲存格式或有不同.
    def _clean_row(row):
        ''' 清除逗號, 清除空白 '''
        for index, content in enumerate(row):
            row[index] = re.sub(",", "", content.strip())
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close' ,'Volume', 'Adj Close']
        res = { fieldnames[0] : row[0],
                fieldnames[1] : row[3],
                fieldnames[2] : row[4],
                fieldnames[3] : row[5],
                fieldnames[4] : row[6],
                fieldnames[5] : row[1],
                fieldnames[6] : row[6] }
        return res

    def _record(stock_id, row):
        downloadFile = os.path.join(downloadDir, "%s.csv"%(stock_id))
        fieldnames = ['Date', 'Open', 'High', 'Low', 'Close' ,'Volume', 'Adj Close']
        # **使用 a+ 的目的**
        # 若該檔案已存在, 則開啟並且將新資料從檔案最末端 append 上去.
        f = open(downloadFile, 'a+')
        # 讀取檔案第一行
        f.seek(0)
        first_line = f.readline()
        f.seek(os.SEEK_END)

        writer = csv.DictWriter(f, fieldnames=fieldnames, lineterminator='\n')
        # 如果檔案裡不存在 'Date', 'Open',...等這些 field, 則寫入這些 field
        if not first_line:
            writer.writeheader()
        # 將剩餘的內容一行行寫入檔案, 並將檔案關閉
        writer.writerow(row)
        f.close()

    def get_stock_data_fields(content):
        # 由於早期網站的資料儲存格式不夠彈性, 導致資料在不同時期被放置在不同 key 內.
        try:
            if content is None:
                return None
            if content['stat'] == '很抱歉，沒有符合條件的資料!' or content['stat'] == '查詢日期大於今日，請重新查詢!':
                print(content['stat'])
                return None

            if 'data5' in content:
                return content['data5']
            else:
                if 'data4' in content:
                    return content['data4']
                else:
                    return content['data2']
        except:
            pprint(content)
            traceback.print_exc()
        return None

    # 從 content 內取出跟各股資訊有關的欄位
    stock_data_fields = get_stock_data_fields(content)
    if not stock_data_fields:
        return False

    try:
        for data in stock_data_fields:
            row = _clean_row([
                '%04d-%02d-%02d'%(year, month, day), # 日期
                data[2], # 成交股數
                data[4], # 成交金額
                data[5], # 開盤價
                data[6], # 最高價
                data[7], # 最低價
                data[8], # 收盤價
                data[3], # 成交筆數
            ])
            _record(data[0].strip(), row)
    except:
        pprint(content)
        traceback.print_exc()
        return False
    return True

def start_download_new_data(date, downloadDir):
    assert isinstance(date, datetime.date), "'date' should be a datetime.date object"
    try:
        res = crawl_tse_data_and_save(downloadDir,\
                                      date.day, date.month, date.year)
        if res:
            print('Download successfully !!')
    except:
        import traceback
        traceback.print_exc()

def try_downloader(date):
    data_folder = os.getcwd()
    downloadDir = os.path.join(data_folder, '%04d-%02d-%02d'%(date.year, date.month, date.day))
    print("Download to folder : {}".format(downloadDir))
    if os.path.exists(downloadDir):
        shutil.rmtree(downloadDir)
    if not os.path.exists(downloadDir):
        os.makedirs(downloadDir)

    # 如果固定下載資料夾(downloadDir), 並用迴圈動態改變 date 的日期
    # 是否可以達成將不同天數的資料寫入同一個檔案中 ?
    start_download_new_data(date, downloadDir)
    print("\nDownload end ~ Bye Bye !")

if __name__ == '__main__':
    args = input('Enter a date for data download, e.g. 2018 1 1\n'
                 'If nothing is entered, today will be used.\n')
    lstArgs = args.split(' ')
    date = datetime.date.today()
    if len(lstArgs) == 3:
        date = datetime.date(int(lstArgs[0]), int(lstArgs[1]), int(lstArgs[2]))
    try_downloader(date)
