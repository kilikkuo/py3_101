import os
from eventloop import EventHandler, shutdown_eventloop
from generaltaskthread import Task, TaskThread
from threading import Lock
from logger import Logger, MSG_INFO, MSG_WARNING, MSG_ERROR, MSG_VERBOSE, MSG_ALL

class RulesMonitor(Logger, EventHandler):
    def __init__(self):
        Logger.__init__(self)
        self.logger_level = MSG_ALL ^ MSG_VERBOSE
        self.verbose("RulesMonitor.__init__")

        EventHandler.__init__(self)
        self.__worker = TaskThread('monitor')
        self.__worker.start()
        self.__is_down = False
        # 一旦收到 'EVT_RULE_CHANGED' 這個事件, 則呼叫 self.__rule_changed 來執行
        # 對應工作
        self.bind('EVT_RULE_CHANGED', self.__rule_changed)

    def __rule_changed(self, *args):
        # 將收到的參數取出, 檢查參數正確性
        assert len(args) == 3, "Rules changed, 3 args expected (rulesetmgr, ticker, tasks)"
        rsmgr = args[0]
        if not rsmgr:
            return
        ticker = args[1]
        tasks = args[2]
        self.verbose("[RuleMonitor] %d tasks for ticker(%s) are going to be dispatched"%(len(tasks), ticker))
        for task in tasks:
            self.__dispatch_rule_task(task)

    def __dispatch_rule_task(self, rule_task):
        # 將任務加到 monitor 執行緒裡進行驗證計算.
        self.__worker.addtask(rule_task)

    def close(self):
        assert not self.__is_down, "Why do you call |close| twice !?"
        self.__shutdown()

    def __shutdown(self):
        self.__worker.stop()
        self.__worker = None
        self.__is_down = True
        self.verbose("RulesMonitor.__shutdown")

gMonitor = None

def start_monitor():
    global gMonitor
    assert not gMonitor, "Monitor exists already, DON'T call this twice (┛`д´)┛"
    gMonitor = RulesMonitor()

def close_monitor():
    global gMonitor
    assert gMonitor, "Call start_monitor() in advance !!"
    gMonitor.close()
    gMonitor = None

"""
#############################################################################
Code below should be used only for unittest !
$> python3 monitor.py
"""
def test_rulemonitor():
    from rulesetmanager import start_rulesetmanager, close_rulesetmanager,\
                                generate_personal_rules, clear_ruleset_pickle,\
                                generate_demo_rules

    # 將既有的 pickled rule 刪除
    clear_ruleset_pickle()
    # 啟動 monitor
    start_monitor()
    # 啟動 rulesetmanager
    start_rulesetmanager()

    # 透過 rulesetmanager 新增/刪除 rules
    generate_personal_rules()
    # generate_demo_rules()

    # 讓主執行緒睡 5 秒, 其他的 worker thread 可以繼續工作
    from time import sleep
    sleep(10)
    # 關閉 monitor
    close_monitor()
    # 關閉 rulesetmanager
    close_rulesetmanager()
    # 將 eventloop 關閉
    shutdown_eventloop()

if __name__ == '__main__':
    test_rulemonitor()
