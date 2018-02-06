import smtplib
from generaltaskthread import TaskThread, Task
from logger import MSG_VERBOSE, MSG_ALL

NOTIFICATION_TYPE_SMS   = 1
NOTIFICATION_TYPE_EMAIL = 2
NOTIFICATION_TYPE_LINE  = 3

USER_TO_EMAIL = { "kilikkuo" : "kilik.kuo@gmail.com" }

def is_network_connected(url=''):
    # 檢查是否有網路連線
    import sys
    if sys.platform in ['darwin', 'linux']:
        # 在 Mac or Linux 上
        DEFAULT_HTTP_SERVER	= 'http://www.google.com/'
        if url == '':
            url = DEFAULT_HTTP_SERVER
        try:
            from urllib import request
            res = request.urlopen(url, timeout = 10.0).read()
            return True
        except:
            pass
    else:
        # 在 Windows 平台
        from ctypes.wintypes import DWORD
        from ctypes import windll, byref, GetLastError
        Sensapi = windll.Sensapi
        flags = DWORD()
        connected = Sensapi.IsNetworkAlive(byref(flags))
        nLastError = GetLastError()
        if nLastError != 0:
            return False
        return bool(connected)
    return False

# 建立一個基礎 Notification 類別, 有一個 notify() 函數可以被不同種類的通知服務實作.
class Notification(Task):
    def __init__(self, notifiees, msg):
        Task.__init__(self)
        self._msg = msg
        self._notifiees = notifiees
    def notify(self):
        raise NotImplementedError
    def run(self):
        self.notify()

# 簡訊通知
class SMSNotification(Notification):
    def __init__(self, notifiees, msg):
        Notification.__init__(self, notifiees, msg)
        pass
    def notify(self):
        # TODO : Implement SMS service
        self.info("SMS::notify(%s):(%s)"%(self._notifiees, self._msg))

# Line bot 通知
class LineNotification(Notification):
    def __init__(self, notifiees, msg):
        Notification.__init__(self, notifiees, msg)
        pass
    def notify(self):
        # TODO : Implement Line service
        self.info("Line::notify(%s):(%s)"%(self._notifiees, self._msg))

# Email 通知
class EmailNotification(Notification):
    def __init__(self, notifiees, msg, smtp_server):
        Notification.__init__(self, notifiees, msg)
        assert smtp_server, "No smtp server, No email notification"
        self.smtp_server = smtp_server
        self.logger_level = MSG_ALL ^ MSG_VERBOSE
        pass

    def notify(self):
        FROM = "Stock Monitor<twstockmonitor@gmail.com>"
        TO = [USER_TO_EMAIL[name] for name in self._notifiees if name in USER_TO_EMAIL]
        SUBJECT = "A Rule Hit"
        TEXT = self._msg
        # 準備郵件
        message = """From: %s\nTo: %s\nSubject: %s\n\n%s
        """ % (FROM, ", ".join(TO), SUBJECT, TEXT)
        try:
            self.info("Email::notify(%s):(%s)"%(self._notifiees, self._msg))

            # 將此段程式碼註解起來, 避免測試階段一直發送測試信件
            # self.smtp_server.sendmail(FROM, TO, message)

            self.verbose("successfully sent the mail")
        except:
            self.error("failed to send mail")

class NotifierThread(TaskThread):
    def __init__(self):
        TaskThread.__init__(self, 'notifier')
        self.__smtp_server = None
        self.__startup_smtp()

    def __startup_smtp(self):
        assert not self.__smtp_server
        if is_network_connected():
            # 請填入自己申請的 mail 信箱
            # https://accounts.google.com/SignUp?hl=zh-TW
            mail_account = ''
            mail_password = ''
            assert mail_account and mail_password, 'Please enter correct ACCOUNT & PWD !!'
            # https://docs.python.org/3/library/smtplib.html
            self.__smtp_server = smtplib.SMTP("smtp.gmail.com", 587)
            self.__smtp_server.ehlo()
            self.__smtp_server.starttls()
            self.__smtp_server.login(mail_account, mail_password)
        else:
            self.log(" No internet connection, SMTP server is not created !", prefixname = True)

    def __create_notification(self, notifiees, nType, msg):
        notification = None
        if (nType == NOTIFICATION_TYPE_SMS):
            notification = SMSNotification(notifiees, msg)
        elif (nType == NOTIFICATION_TYPE_EMAIL):
            notification = EmailNotification(notifiees, msg, self.__smtp_server)
        elif (nType == NOTIFICATION_TYPE_LINE):
            notification = LineNotification(notifiees, msg)
        else:
            assert False, "Not corresponding notfication type !"
        return notification

    def __close_smtp(self):
        # 將 smtp server 的連線關閉
        if self.__smtp_server:
            self.__smtp_server.close()
        self.__smtp_server = None

    def shutdown(self):
        self.__close_smtp()
        self.stop()

nt = None

def start_notifier():
    global nt
    assert nt == None, "Notifier already exists ... check your code !"
    # 建立 NotifierThread 並且啟動
    nt = NotifierThread()
    nt.start()

def add_notification(notifiees, types, message):
    global nt
    assert nt, "Notifier doesn't exist, nothing to do"

    # 依據參數的種類建立要被執行的 Notification 任務
    # 並將 task 加入到 notifier 執行緒裡.
    for nType in types:
        notification = nt._NotifierThread__create_notification(notifiees, nType, message)
        nt.addtask(notification)

def stop_notifier():
    global nt
    assert nt, "Notifier doesn't exist, nothing to do"
    nt.shutdown()
    nt = None

if __name__ == '__main__':
    start_notifier()
    add_notification(["kilikkuo"],\
                     [NOTIFICATION_TYPE_EMAIL],\
                      "Haha")
    from time import sleep
    sleep(5)
    stop_notifier()
