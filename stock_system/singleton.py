import threading
class Singleton(type):
    __instance = None
    __ref_count = 0
    __lock = threading.RLock()
    def __call__(cls, *args, **argd):
        with cls.__lock:
            if not cls.__instance:
                cls.__instance = super(Singleton, cls).__call__(*args, **argd)
            cls.__ref_count += 1
            return cls.__instance

    def close(cls):
        """
        Derived class needs to call this method to decrease refcount.
        Derived class should check the returned value for cleaning up its internal data.
        """
        with cls.__lock:
            cls.__ref_count -= 1
            assert cls.__ref_count >=0, "Too many close for %s, check !!"%(str(cls))
            if cls.__ref_count == 0:
                cls.__instance = None
                return True
            return False

    def can_shutdown(cls):
        """
        Derived class should ask this for cleanup its internal data.
        """
        return cls.__ref_count == 0

    def __del__(cls):
        assert cls.__ref_count == 0, "%s is not closed properly, un-paired creation & close"%(str(cls))

class Child(metaclass=Singleton):
    def __init__(self):
        # Allocate internal resources
        print(' Child.__init__ ')
        pass

    def __shutdown(self):
        # Release internal resources.
        pass

    def close(self):
        if Singleton.close(Child):
            self.__shutdown()

if __name__ == "__main__":
    def create_child(i):
        import time
        import random
        c = Child()
        # print('{}'.format(i))
        rand = random.random()
        time.sleep(rand)
        c.close()
    # 第 1 次 'Child.__init__' 被印出來
    from concurrent.futures import ThreadPoolExecutor
    workers = 10000
    executor = ThreadPoolExecutor(max_workers=workers)
    for i in range(workers):
        executor.submit(create_child, i)
    executor.shutdown()
    # 所有 worker 都執行結束

    # 第 2 次 'Child.__init__' 被印出來
    c = Child()
    c_leaked = Child()
    c.close()
    # NOTE : 如果不呼叫 c_leaked.close() 將會產生 exception !
    # c_leaked.close()
    pass
