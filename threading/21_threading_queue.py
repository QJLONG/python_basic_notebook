import queue

# Queue队列 先进先出（FIFO）即First In First Out
q = queue.Queue()

q.put('First')
q.put('Second')
q.put('Third')

print(q.get())
print(q.get())
print(q.get())

print('*'*50)

# 栈 后进先出（LIFO）即Last In First Out
q2 = queue.LifoQueue()

q2.put('First')
q2.put('Second')
q2.put('Third')

print(q2.get())
print(q2.get())
print(q2.get())

print('*'*50)
# 自定义存储顺序 值小的先取出  传入的参数是元组
q3 = queue.PriorityQueue()

q3.put((2,'a'))
q3.put((1,'b'))
q3.put((3,'c'))

print(q3.get())
print(q3.get())
print(q3.get())

# 三种序列的共有方法
print(q._qsize()) # 返回队列大小
print(q.full())  # 是否满
print(q.empty()) # 是否空

