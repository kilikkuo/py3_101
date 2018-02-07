import os
import pickle
import datetime
from singleton import Singleton
from logger import Logger, MSG_INFO, MSG_WARNING, MSG_ERROR, MSG_VERBOSE, MSG_ALL
from pprint import pprint
from eventloop import EventHandler, shutdown_eventloop
from generaltaskthread import Task
from sourcedatabank import SourceDataBank
# 等到 Notifier 有自己的 email 通知服務的帳號/密碼之後即可將這段程式碼打開
# from notifier import add_notification, NOTIFICATION_TYPE_EMAIL

CONDITION_NONE  = 0
CONDITION_RSI   = 1

def cond_type_to_name(cond_type):
    if cond_type == CONDITION_NONE:
        return "None"
    elif cond_type == CONDITION_RSI:
        return "RSI"
    return "Unknown"

class Condition(Task):
    """
    Condition 任務只包含了哪些指標要測試, 以及要測試的條件為何
    真正的股價的提取與指標的計算都會等到 Condition Task 在執行時才會真正進行.
    """
    cond_type = CONDITION_NONE
    def __init__(self, sdb, ticker, base, statement, pivot):
        Task.__init__(self)
        assert type(ticker) == str, "[%s] ticker should be str"%(cond_type_to_name(self.cond_type))
        assert type(statement) == str, "[%s] statement should be str"%(cond_type_to_name(self.cond_type))
        assert type(base) == str, "[%s] base should be str"%(cond_type_to_name(self.cond_type))
        assert base in ["week", "day", "quarter"]
        self.sdb = sdb
        self.ticker = ticker
        # Statement 為一個字串, 描述指標大於or小於多少數值
        self.statement = statement
        # 指標計算的基數, 以"天","周","月"
        self.base = base
        # 指標計算的起始日
        self.pivot = pivot
    def update_info(self, base = None, pivot = None, statement = None):
        # 提供函數來更新 Condition Task 內部的資料
        if base:
            self.base = base
        if pivot:
            self.pivot = pivot
        if statement:
            self.statement = statement
    def _verify(self):
        raise NotImplementedError
    def run(self):
        self.verbose("[%s][%s] verifying ... "%(self.get_current_thread_name(), cond_type_to_name(self.cond_type)))
        return self._verify()

class RSICondition(Condition):
    cond_type = CONDITION_RSI
    def __init__(self, sdb, ticker, base, statement, unit, price_at = "close", pivot = datetime.date.today()):
        Condition.__init__(self, sdb, ticker, base, statement, pivot)
        self.logger_level = MSG_ALL ^ MSG_VERBOSE ^ MSG_WARNING
        self.unit = unit
        self.price_at = price_at

    def _verify(self):
        from rsi import calc_smooth_rsi, SMOOTH_RSI_FACTOR
        from functools import reduce
        result = False
        try:
            # TODO : Need to handle different base : "week" / "quarter"
            # 目前只支援以"天數"為基礎的 RSI 計算
            assert self.base == "day"
            prices, dates = self.sdb.get_prices(self.ticker, self.unit * SMOOTH_RSI_FACTOR,\
                                                price_at = self.price_at,
                                                pivot = self.pivot)
            if prices == []:
                self.warning("No price data in SDB, skip it")
                return False
            # 將價格串列從舊到新排序
            prices_old_to_new = list(reversed(prices))
            rsi = calc_smooth_rsi(self.unit, prices_old_to_new)

            self.verbose("rsi=%f"%(rsi))
            # 將 statement 中的特殊符號做轉換, 並且進行值計算
            replaced_cond = self.statement.replace("@", "%f"%(rsi))
            result = eval(replaced_cond)
            self.verbose("[%s][%s] Verifying ... base(%s)/unit(%d)/statement(%s)/result(%d)"%(\
                        self.ticker, self.pivot, self.base, self.unit, self.statement, result))
        except:
            self.error('[{}] RSI error - start from {}'.format(self.ticker, self.pivot))
        return result

def create_tasks_from_conditions(sdb, ticker, conditions):
    """ Examples
    Reference : get_sample_conditions_for_backtest()
    """
    tasks = []
    for cond in conditions:
        # 檢查每一個 condition 的資料, 是否為支援的技術指標
        cond_idx = cond.get("index", None)
        if not cond_idx:
            continue

        task = None
        if cond_idx == "rsi":
            # 如果是 RSI 技術指標, 將其對應的計算條件組合成 RSICondition
            task = RSICondition(sdb, ticker,\
                                cond.get("base", ""),\
                                cond.get("statement", None),
                                cond.get("unit", ""),
                                price_at = cond.get("price_at", "close"),
                                pivot = cond.get("pivot", datetime.date.today()))
        else:
            continue
        tasks.append(task)
    assert len(tasks) != 0
    return tasks

class Verification(Task):
    def __init__(self, sdb, ticker, conditions, notifiees, desc, pivot = datetime.date.today()):
        Task.__init__(self)
        self.ticker = ticker
        # 將各種技術指標的驗證規則資料透過 create_tasks_from_conditions() 建立
        # 對應的任務串列
        self.tasks = create_tasks_from_conditions(sdb, ticker, conditions)
        self.notifiees = notifiees
        self.pivot = pivot
        self.desc = desc

    def run(self):
        self.verify()

    def verify(self):
        results = []
        # 透過迴圈, 將多個指標的驗證計算任務逐一執行, 並且將每一個驗證結果儲存在 results
        # list.
        for rule_condition in self.tasks:
            ref_info = {'pivot' : self.pivot}
            rule_condition.update_info(**ref_info)
            results.append(rule_condition.run())

        # 透過 reduce 將串列裡的每一項結果逐一交集, 取得最後結果.
        from functools import reduce
        final_result = reduce(lambda x, y: x and y, results)

        if final_result:
            color_code_prefix = "\033[1;33m" if self.desc == "entry" else "\033[1;34m"

            tname = '台灣50' if self.ticker == '0050' else '未知'
            msg = '{}TICKER({})({:6s}) => {} \033[m'.format(color_code_prefix, self.ticker, tname, self.desc)

            print('msg : {}'.format(msg))
            '''
            # 等到 Notifier 有自己的 email 通知服務的帳號/密碼之後即可將這段程式碼打開
            # add_notification(self.notifiees,\
            #                  [NOTIFICATION_TYPE_EMAIL],\
            #                  msg)
            '''
        pass

class RulesetManager(Logger, EventHandler, metaclass=Singleton):
    def __init__(self):
        Logger.__init__(self)
        self.logger_level = MSG_ALL
        self.verbose("RulesetManager.__init__")

        EventHandler.__init__(self)
        self.is_strategies_loaded = False
        self._sdb = SourceDataBank()
        self.__strategies_file = os.path.join(os.getcwd(), "rs.p")
        self.bind("DOWNLOAD_UPDATE_COMPLETED", self.__on_data_updated)
        """
        # self.__strategies 是一個 dictionary 結構, 存放針對每一個股票的各種策略
        { 'ticker' : { 1 : strategy_info1, 2 : strategy_info2, ...},
          'max_strategy_id' : 3,
        }

        # strategy_info1 包含以下結構, 股票名, conditions串列, 要通知的對象, 進出場說明.
        { 'ticker'  : ticker in string,
          'conditions' : list of conditions,
          'notifiees'  : list of notifiees,
          'desc'    : 描述進出場的文字
        }

        # 一個 condition set 的資料必須包含以下三個 keys
        1) base : 指定要計算的指標的基礎單位, i.e. "day", "week", "quarter".
        2) statement : 用來計算驗證結果的表示式. 使用 "@" 做為計算完的值的取代符
                       e.g. success = eval('@>=20'.replace('@', calucated_value()))
        3) index : 指定使用何種技術指標, i.e. "rsi", "ma", "kd"...
        e.g. cond_set = { "index"   : "rsi",
                          "statement" : "@>=2",
                          "base"    : "day",
                          "unit"    : 10}
        """

        self.__strategies = {}
        self.__max_strategy_id = 0
        """
        # self.__ticker2tasks 存放目前針對某 ticker 應該執行哪些策略任務
        { 'ticker' : { 1 : task1, 2 : task2, ...},
        }
        # task1, task2 are strategy tasks.
        """
        self.__ticker2tasks = {}
        self.__load(self.__strategies_file)

    def __on_data_updated(self):
        # 一旦 SourceDataBank 有資料更新, 即將現有的所有策略都丟給 Monitor 重新驗證一次.
        self.info("New data is updated to SDB, sending strategy tasks to verify !!")
        self.__send_tasks_to_monitors()
        pass

    def __create_strategy_task(self, strategy_info):
        # strategy_info 是一個 dictionary 的資料結構, 將 strategy_info 轉換成
        # Verification 任務
        assert "conditions" in strategy_info, "strategy_info should contain conditions."
        assert "ticker" in strategy_info, "strategy_info should contain ticker."
        assert "notifiees" in strategy_info, "strategy_info should contain notifiees."

        ticker = strategy_info["ticker"]
        conditions = strategy_info["conditions"]
        notifiees = strategy_info["notifiees"]
        desc = strategy_info["desc"]

        task = Verification(self._sdb, ticker, conditions, notifiees, desc)
        return task

    def __load(self, filename):
        assert not self.is_strategies_loaded, "Strategy set should not be loaded twice !"

        if not os.path.isfile(filename) and not os.path.exists(filename):
            self.verbose("Presumming it's your 1st time ... nothing to load in")
        else:
            try:
                self.__strategies = pickle.load(open(filename, "rb"))
            except:
                self.error("Failed to load strategies pickle (%s)!!"%(filename))
                return
        self.__max_strategy_id = self.__strategies.get('max_strategy_id', 0)
        self.__prepare_strategy_tasks()

        self.info(" <<<<<< Strategy set loaded >>>>>>")
        self.is_strategies_loaded = True
        self.__send_tasks_to_monitors()
        pass

    def get_unique_strategy_id(self):
        self.__max_strategy_id += 1
        self.__strategies['max_strategy_id'] = self.__max_strategy_id
        sid = self.__max_strategy_id
        return sid

    def __save(self):
        assert self.is_strategies_loaded, "Straties should be loaded first !"
        pickle.dump(self.__strategies, open(self.__strategies_file, "wb"))
        pass

    def add_strategy(self, ticker, conditions, notifiees, desc,\
                 price_at = "close"):
        assert self.is_strategies_loaded, "Cannot add strategy now !"
        # TODO : 1) Consider thread safty,
        #        2) Design condition str for each cond_type
        """
        Strategy - http://reader.roodo.com/brysonbo/archives/4225907.html
        Knowledge - http://blog.roodo.com/brysonbo/archives/4225941.html
        BIAS       - http://www.angelibrary.com/economic/gsjs/045.htm
        KD         - http://www.angelibrary.com/economic/gsjs/044.htm
        """
        sid = 0
        try:
            strategy_info = {}
            strategy_info['ticker'] = ticker
            strategy_info["conditions"] = conditions
            strategy_info["price_at"] = price_at
            strategy_info["notifiees"] = notifiees
            strategy_info["desc"] = desc

            ticker_strategies = self.__strategies.setdefault(ticker, {})
            sid = self.get_unique_strategy_id()
            assert sid not in ticker_strategies, "sid already exists ~ !0o0!"
            ticker_strategies[sid] = strategy_info

            task = self.__create_strategy_task(strategy_info)
            self.__add_strategy_task_to_list(ticker, sid, task)
        except AssertionError as ae:
            self.error(ae.args)
            sid = 0
        return sid

    def delete_strategy(self, ticker, sid):
        assert self.is_strategies_loaded, "Cannot delete strategy now !"
        if ticker not in self.__strategies:
            return False
        strategy_info = self.__strategies[ticker].pop(sid)
        if strategy_info:
            self.__delete_strategy_tasks_from_list(ticker, sid)
            return True
        return False
        pass

    def __get_strategy_tasks(self, ticker):
        dict_tasks = self.__ticker2tasks.get(ticker, {})
        tasks = list(dict_tasks.values())[:]
        return tasks

    def print_strategies(self, ticker = None):
        if ticker:
            pprint(self.__strategies.get(ticker, None))
        else:
            pprint(self.__strategies)

    def close(self):
        Singleton.close(RulesetManager)
        if Singleton.can_shutdown(RulesetManager):
            self.__shutdown()
        pass

    def __add_strategy_task_to_list(self, ticker, rid, task):
        dict_tasks = self.__ticker2tasks.setdefault(ticker, {})
        dict_tasks[rid] = task

        now_tasks = self.__get_strategy_tasks(ticker)
        self.info(" >>>> __add_strategy_task_to_list ... len_of_tasks(%d)"%(len(now_tasks)))
        self.invoke("EVT_RULE_CHANGED", self, ticker, now_tasks)

    def __delete_strategy_tasks_from_list(self, ticker, sid):
        self.__ticker2tasks[ticker].pop(sid)
        now_tasks = self.__get_strategy_tasks(ticker)
        self.info(" >>>> __delete_strategy_tasks_from_list")
        self.invoke("EVT_RULE_CHANGED", self, ticker, now_tasks)

    def __prepare_strategy_tasks(self):
        for ticker, strategies in self.__strategies.items():
            if type(strategies) == dict:
                for sid, info in strategies.items():
                    task = self.__create_strategy_task(info)
                    self.__ticker2tasks.setdefault(ticker, {})[sid] = task
        pass

    def __send_tasks_to_monitors(self):
        self.info(" >>>> __send_tasks_to_monitors")
        if not self.__strategies:
            self.warning("No strategy tasks to be dispatched ... ")
        for ticker, strategies in self.__strategies.items():
            if type(strategies) == dict:
                now_tasks = self.__get_strategy_tasks(ticker)
                self.invoke("EVT_RULE_CHANGED", self, ticker, now_tasks)

    def __shutdown(self):
        self.__save()
        self._sdb.close()
        self._sdb = None
        self.verbose("RulesetManager.__shutdown")
        pass

gRSMgr = None
def __start_rulesetmanager():
    global gRSMgr
    assert not gRSMgr, "RulesetManager exists already, DON'T call this twice (┛`д´)┛"
    gRSMgr = RulesetManager()

def __close_rulesetmanager():
    global gRSMgr
    assert gRSMgr, "Call start_rulesetmanager() in advance !!"
    gRSMgr.close()
    gRSMgr = None

def start_rulesetmanager():
    # Should be called only in monitor.
    # 其他檔案透過以下程式碼
    # '''
    # from rulessetmanager import start_rulesetmanager
    # start_rulesetmanager()
    # '''
    # 便會始 RulesetManager 被初始化, 並且使得 gRSMgr 不為 None
    # 這樣的設計目的是希望此函數 start_rulesetmanager 只在某一個地方被某一個物件初始
    globals()['__start_rulesetmanager']()

def close_rulesetmanager():
    # Should be called only in monitor.
    globals()['__close_rulesetmanager']()

# Public method for other modules.
def add_strategies_to_rulesetmanager(ticker, conditions, notifiees, desc):
    global gRSMgr
    assert gRSMgr, "Call start_rulesetmanager() in advance !!"
    assert type(conditions) == list
    assert type(notifiees) == list  # e.g. ["johnhu", "tommykuo"]

    sid = gRSMgr.add_strategy(ticker, conditions, notifiees, desc)
    if sid == 0:
        print("[Error] add_strategies_to_rulesetmanager failed ... ")
    return sid

# Public method for other modules.
def delete_strategies_from_rulesetmanager(ticker, sid):
    global gRSMgr
    assert gRSMgr, "Call start_rulesetmanager() in advance !!"
    assert sid > 0, "Invalid rid"
    result = gRSMgr.delete_strategy(ticker, sid)
    if not result:
        print("[Error] delete_strategies_from_rulesetmanager failed ... ")
    return result

"""
#############################################################################
Code below should be used only for unittest !
$> python3 rulesetmanager.py
"""

def clear_ruleset_pickle():
    cwd = os.getcwd()
    rule_file = os.path.join(cwd, 'rs.p')
    if os.path.exists(rule_file):
        os.remove(rule_file)

def generate_personal_rules():
    # RSI 相關 =====================================================
    cond_set1 = { "unit"    : 5,
                  "index"   : "rsi",
                  "statement" : "@<=30",
                  "base"    : "day"}
    cond_set2 = { "unit"    : 5,
                  "index"   : "rsi",
                  "statement" : "@>=70",
                  "base"    : "day",
                  "price_at"   : "close"}

    ticker = '0050'
    rid1 = add_strategies_to_rulesetmanager(ticker,\
                                            [cond_set1],\
                                            ["kilikkuo"],\
                                            "entry")
    assert rid1 != 0, "rid1 should not be zero."

    rid2 = add_strategies_to_rulesetmanager(ticker,\
                                            [cond_set2],\
                                            ["kilikkuo"],\
                                            "exit")

    assert rid2 != 0, "rid should not be zero."
    assert rid1 != rid2, "rid1 should not be rid2."

    result = delete_strategies_from_rulesetmanager(ticker, rid2)
    assert result, "Stragety should be deleted successfully."

    pass

def generate_demo_rules():
    # RSI 相關 =====================================================
    cond_set1 = { "unit"    : 5,
                  "index"   : "rsi",
                  "statement" : "@<=30",
                  "base"    : "day"}
    cond_set2 = { "unit"    : 5,
                  "index"   : "rsi",
                  "statement" : "@>=70",
                  "base"    : "day",
                  "price_at"   : "close"}

    tickers = ['5285', '4164', '4904', '2356', '6168', '1314', '2886', '2823',
               '2015', '2353', '6552', '3044', '6183', '4958', '2816', '9910',
               '1303', '3130', '3583', '8464', '6177', '6415', '3006', '5906',
               '6213', '1218', '1506', '1760', '2516', '2855', '3653', '1236',
               '3060', '3406', '6230', '4190', '3046', '1711', '2332', '2108',
               '1235', '8105', '1473', '6145', '4968', '1605', '2375', '2901',
               '1906', '3058']

    for ticker in tickers:
        rid1 = add_strategies_to_rulesetmanager(ticker,\
                                                [cond_set1],\
                                                ["kilikkuo"],\
                                                "entry")
        assert rid1 != 0, "rid1 should not be zero."

        rid2 = add_strategies_to_rulesetmanager(ticker,\
                                                [cond_set2],\
                                                ["kilikkuo"],\
                                                "exit")

        assert rid2 != 0, "rid should not be zero."
        assert rid1 != rid2, "rid1 should not be rid2."

    pass

if __name__ == "__main__":
    clear_ruleset_pickle()
    demo_all = False
    if demo_all:
        from sourcedatabank import prepare_sourcedatabank_for_all
        prepare_sourcedatabank_for_all()

    globals()['__start_rulesetmanager']()
    # NOTE: Create your own rules
    if demo_all:
        generate_demo_rules()
    else:
        generate_personal_rules()
    globals()['__close_rulesetmanager']()
    shutdown_eventloop()