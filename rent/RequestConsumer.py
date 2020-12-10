from threading import Thread, Lock, Condition
import queue
import time
import random

queue = queue.Queue(10)


class OnlyOne(object):
    class __OnlyOne:
        def __init__(self):
            self.val = None

        def __str__(self):
            return repr(self) + self.val

    instance = None

    def __new__(cls):  # __new__ always a classmethod
        if not OnlyOne.instance:
            OnlyOne.instance = OnlyOne.__OnlyOne()
        return OnlyOne.instance

    def __getattr__(self, name):
        return getattr(self.instance, name)

    def __setattr__(self, name):
        return setattr(self.instance, name)


# if __name__ == '__main__':
#     print('test')
#     ProducerThread().start()
#     ConsumerThread().start()


class ProducerThread(Thread):
    a = 1

    def run(self):
        nums = range(5)
        global queue
        while True:
            num = random.choice(nums)
            queue.put(num)
            print("Produced", num)
            time.sleep(random.random())


class ConsumerThread(Thread):

    def fun1():
        while True:
            num = queue.get()
            queue.task_done()
            print("Consumed", num)
            time.sleep(random.random())


    Thread(target=fun1).start()
