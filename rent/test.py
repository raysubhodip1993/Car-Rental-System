from rent import RequestConsumer
from threading import Thread, Lock, Condition

a = RequestConsumer.OnlyOne()
a.val = 'test'
print(a)

b= RequestConsumer.OnlyOne()
b.val = b.val+'qw'

print(b)

# thread1 = Thread(target=fun1, args=(12, 10))
# thread1.start()
RequestConsumer.ConsumerThread()
RequestConsumer.queue.put("test1")
RequestConsumer.queue.put("test1")
RequestConsumer.queue.put("test1")
RequestConsumer.queue.put("test1")




# b = RequestConsumer.OnlyOne('chuchra')
# print(b.val)

#
# # rr = RequestConsumer.startThreads()
# # RequestConsumer.ProducerThread()
# # rr.queue.put('vsu')
#
#
# c = RequestConsumer.ConsumerThread()
# r = RequestConsumer.ProducerThread()
#
# print(c.b)
# print(r.a)
#
# c.b =56
#
# x = RequestConsumer.ConsumerThread()
# print(x.b)
#
# # print(RequestConsumer.queue)
# #
# #
# # c.run()
# # r.run()
# #
# # RequestConsumer.queue.put('vsu')
# # print(RequestConsumer.queue)
#
#
#
# class Singleton(type):
#     _instances = {}
#     def __call__(cls, *args, **kwargs):
#         if cls not in cls._instances:
#             cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
#         return cls._instances[cls]