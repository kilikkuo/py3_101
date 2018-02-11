import os
import csv
import pickle
import datetime
from pprint import pprint
from threading import Lock
from singleton import Singleton

def debug_print(msg):
    if False:
        print('[sourcedatabank.py] ' + msg)

def read_ticker_CSV(csvPath):
    """
    回傳一個 dictionary-like 的資料結構,
    Returned data will be dictionary-like. The OLDER data with the SMALLER index.
    {'1101': {0: {'date' : '2003-06-30', 'close': 35.0, ...},
              1: {'date' : '2003-07-01', 'close': 35.0, ...},
              ...
              'end': '2016-08-15',
              'start': '2016-08-11'}}
    """
    assert os.path.isfile(csvPath), "File(%s) does NOT exist !"%(csvPath)
    ticker = os.path.splitext(os.path.basename(csvPath))[0]

    with open(csvPath, 'r', encoding='utf8') as f:
        csv_data = csv.DictReader(f)
        start = None
        end = None
        dic_raw_data = {}
        dic_inner_data = {}
        for idx, row in enumerate((list(csv_data))):
            lower_row = dict((k.lower(), v) for k, v in row.items())
            has_exception = False
            for k, v in lower_row.items():
                try:
                    if k != "date" and v is not None:
                        lower_row[k] = float(v)
                except:
                    has_exception = True
                    debug_print('Excetpion while reading csv data, k = {}, v = {}'.format(k, v))
                    pass
            try:
                if lower_row['volume'] == 0 or has_exception:
                    # 如果當日沒有交易量, 則不需要將資料放入 SourceDataBank, 因為無意義.
                    # 如果讀取 row 有問題, 例如沒有價格, 也不要放入資料庫
                    continue
            except:
                debug_print('Excetpion while reading csv data, row = {}'.format(lower_row))
                continue

            dic_inner_data[idx] = lower_row
            start = lower_row['date'] if start == None else min(start, lower_row['date'])
            end = lower_row['date'] if end == None else max(end, lower_row['date'])

        # debug_print(' {}, start({}) to end({}), Number of Row : {}'.format(ticker, start,\
        #         end, len(dic_inner_data)))
        dic_inner_data['end'] = end
        dic_inner_data['start'] = start
        dic_raw_data[ticker] = dic_inner_data
        return dic_raw_data
    return None

class SourceDataBank(metaclass=Singleton):
    """
    讀取/更新/etc...等操作應該保證是 thread-safe. 因為任何 task 可能在不同的 thread
    裡對 SourceDataBank 執行操作
    """
    def __init__(self, data_folder=None):
        debug_print("SourceDataBank.__init__")

        """
        1) 如果程序裡 SDB 已經被起始過, 則 __init__ 將不會再被呼叫.
        2) self.__src_data is a dictionary-like datastruture.
            {'1101': {'date1' : {'closes' : P1, 'opens' : P2, ...}, },
                      'date2' : {'closes' : P3, 'opens' : P4, ...},
                      ...
                      'end': '2016-08-15',
                      'start': '2016-08-11'}}
        """
        cwd = os.getcwd()
        if data_folder and os.path.isdir(data_folder):
            self.data_folder = data_folder
        else:
            # 預設寫死 2018-02-02, 可改作為動態輸入
            self.data_folder = os.path.join(cwd, '%04d-%02d-%02d_0050'%(2018, 2, 2))
        # pickled file 名稱為 sourcedata.p
        self.source_bank_file = os.path.join(cwd, "sourcedata.p")
        # 資料是否已載入完成
        self.is_src_loaded = False
        # 資料是否已正在更新
        self.is_updating = False
        # 用來保護 operation 完整性的鎖
        self.op_lock = Lock()

        self.__src_data = {}
        self.__startup()
        pass

    def __startup(self):
        assert not self.is_src_loaded, "Should not startup twice !!"
        # 將 pickled 資料載入程式
        self.__load_from_pickle()

    def __load_from_pickle(self):
        if not os.path.exists(self.source_bank_file) and not os.path.isfile(self.source_bank_file):
            # 如果 pickled 檔案不存在, 或不是一個檔案, 表示第一次載入!
            debug_print("Presumming it's your 1st time ... nothing to load in")
            self.__src_data.clear()
            # 利用下載下來的 csv 重新載入
            self.__reload_from_csv()
        else:
            try:
                # 從 pickled 檔案載入
                self.__src_data = pickle.load(open(self.source_bank_file, "rb"))
            except:
                debug_print("Failed to load src pickle !!")
                return

        # TODO : 如何驗證資料的一致性 ?
        #        1) sourcedata.p 是否遭到破壞
        #        2) sourcedata.p 是否跟現有的 csv files 的資料一致

        self.is_src_loaded = True
        debug_print("Loading SourceDataBank data completed !")
        pass

    def __reload_from_csv(self):
        for root, dirs, files in os.walk(self.data_folder):
            if root == self.data_folder:
                files.sort()
                # 將資料夾底下的所有 csv 檔案, 一個個讀入
                for basename in files:
                    filename = os.path.join(root, basename)
                    debug_print('filename : {}'.format(filename))
                    ticker_new_data = read_ticker_CSV(filename)
                    self.__update(ticker_new_data)
                break
        debug_print("Reload SourceDataBank data from CSV completed !")

    def __update(self, raw_data):
        # Iterate each new ticker data, and update into src data accroding to datetime
        for ticker, info in raw_data.items():
            new_start = info['start']
            new_end = info['end']
            ticker_src_data = self.__src_data.get(ticker, {})

            # =================================================================
            # NOTE: 此區段為錯誤檢查程式, 檢查每一股資料的最早與最遠資料日期是否存在與正確
            src_start = ticker_src_data.get("start", new_start)
            src_end = ticker_src_data.get("end", new_end)
            if not src_start or not src_end:
                debug_print("[%s] No Src start date or end date - continue "%(ticker))
                continue
            if not new_start or not new_end:
                debug_print("[%s] No New start date or end date - continue "%(ticker))
                continue
            final_start = min(src_start, new_start)
            final_end = max(src_end, new_end)
            # =================================================================

            # 重新將更正過後的起始日與最後日資料組合
            for idx, data in info.items():
                if idx == "end":
                    ticker_src_data["end"] = final_end
                elif idx == "start":
                    ticker_src_data["start"] = final_start
                else:
                    date_info = ticker_src_data.setdefault(data["date"], {})
                    if date_info:
                        assert date_info["vols"] == data["volume"] and\
                                date_info["closes"] == data["close"] and\
                                date_info["opens"] == data["open"] and\
                                date_info["lows"] == data["low"] and\
                                date_info["highs"] == data["high"], "Updating conflicted data for same date(%s) !"%(data["date"])
                    date_info["vols"] = data["volume"]
                    date_info["closes"] = data["close"]
                    date_info["opens"] = data["open"]
                    date_info["lows"] = data["low"]
                    date_info["highs"] = data["high"]

            self.__src_data[ticker] = ticker_src_data
        # pprint(self.__src_data)

    def update(self, raw_data):
        # 透過 updater 來更新 SDB 裡的資料
        assert self.is_src_loaded, "Should be called after src data loaded !"
        assert not self.is_updating, "Should not be updating !"
        # 利用鎖將此操作保護住, 避免在更新時有其他執行緒也來更新.
        with self.op_lock:
            try:
                self.is_updating = True
                self.__update(raw_data)
            except AssertionError as ae:
                debug_print("During updating, going to rollback now : %s"%(ae.args))
                # 若操作發生錯誤, 回溯資料
                self.__rollback()
                raise ae
            finally:
                self.is_updating = False
        pass

    def get_prices(self, ticker, days, price_at="close", pivot = datetime.date.today()):
        '''
        :rtype: List[int], List[str]
        # 取得兩個 list, 一個是價格 list, 一個是日期 list,
        # 起始日為設定的 pivot, 並且包含從該日開始的前 days 日價格.
        # 簡單來說就是從最近的到最早的價格.
        # e.g. pivot = 2018-02-02,  days = 4
        # 得到  [10,           11,           10.4,         12]
        #      ['2018-02-02', '2018-02-01', '2018-01-31', '2018-01-30']
        '''
        with self.op_lock:
            ticker_data = self.__src_data.get(ticker, {})
            if not ticker_data:
                debug_print("No ticker_data for ticker(%s) "%(ticker))
                return [], []
            start = ticker_data.get("start", "")
            end = ticker_data.get("end", "")
            count = days
            strpivot = '%04d-%02d-%02d'%(pivot.year, pivot.month, pivot.day)
            if  strpivot < start or strpivot > end:
                # 檢查 pivot date 是否超過最早或最晚的資料日
                debug_print("Pivot(%s) is not in existing period. S(%s)=>E(%s) "%(strpivot, start, end))

            dates = [date for date in ticker_data if date not in ["start", "end"]]
            # 經過 sort 後, 日期為由離現在近到遠
            dates.sort(reverse = True)

            found = False
            price_key = price_at.lower() + 's'
            prices = []
            ret_dats = []
            # 開始掃描資料庫中該股的所有資料, 找到對應 pivot day 的那天股價並紀錄起來,
            # 然後在往後找目標天數的資料.
            for i, date in enumerate(dates):
                if date == strpivot:
                    found = True
                    prices.append(ticker_data[date][price_key])
                    ret_dats.append(date)
                    count -= 1
                elif date < strpivot:
                    if not found:
                        found = True
                        debug_print("Pivot doesn't match exactlly, find closest one(%s)!!"%(date))
                    prices.append(ticker_data[date][price_key])
                    ret_dats.append(date)
                    count -= 1
                if count == 0:
                    break

            if len(prices) != days:
                debug_print("Length(%d) of prices doesn't match expected days(%d) !!"%(len(prices), days) +
                      "(%s, %s)"%(ticker, strpivot))
            return prices, ret_dats

    def __rollback(self):
        # 清除所有成是在記憶體內的資料, 重新從檔案存取.
        self.__src_data.clear()
        self.__load_from_pickle()

    def close(self):
        Singleton.close(SourceDataBank)
        if Singleton.can_shutdown(SourceDataBank):
            self.__shutdown()

    def __shutdown(self):
        # Only when last SDB instance calls close()
        assert self.is_src_loaded, "Should not called __shutdown before __startup !!"
        assert not self.is_updating, "SDB cannot shutdown while updating !!"
        pickle.dump(self.__src_data, open(self.source_bank_file, "wb"))
        self.__src_data.clear()
        debug_print("SourceDataBank.__shutdown")
        pass

"""
#############################################################################
$> python3 sourcedatabank.py
"""
def prepare_sourcedatabank_for_test():
    cwd = os.getcwd()
    # 先刪除 sourcedata.p 以便執行乾淨環境的測試
    source_bank_file = os.path.join(cwd, 'sourcedata.p')
    if os.path.exists(source_bank_file):
        os.remove(source_bank_file)

    # 第一次載入資料, 讀取 0050.csv.
    sdb = SourceDataBank()
    # 讀取 0051 的資料並且更新進 SDB
    path = os.path.join(cwd, '2018-02-02_0051', '0051.csv')
    data_20180202_0051 = read_ticker_CSV(path)
    sdb.update(data_20180202_0051)
    sdb.close()

    # 讀取 0051 的 包含(2018,1,29) 之前的 3 天股價資料, 並且驗證是否正確
    sdb = SourceDataBank()
    prices, dates = sdb.get_prices('0051', 3, 'open', datetime.date(2018,1,29))
    assert [32.54, 32.44, 32.75] == prices, "[Unexpected] date(2018,1,29) prices = {}".format(prices)
    assert ['2018-01-29', '2018-01-26', '2018-01-25'] == dates, '[Unexpected] dates'
    sdb.close()
    print('[SourceDataBank] Test Completed !!')

def prepare_sourcedatabank_for_all():
    cwd = os.getcwd()
    # 先刪除 sourcedata.p 以便執行乾淨環境的測試
    source_bank_file = os.path.join(cwd, 'sourcedata.p')
    if os.path.exists(source_bank_file):
        os.remove(source_bank_file)

    sdb = SourceDataBank(os.path.join(cwd, '2018-02-02_all'))
    # 讀取 2018-02-02_all 資料夾下所有資料並且更新進 SDB
    sdb.close()
    print('[SourceDataBank] All data prepared !!')

if __name__ == "__main__":
    prepare_sourcedatabank_for_test()
