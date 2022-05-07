import threading
import queue
import time

# create a producter method
def producter(name):
    count = 1
    # creating products
    while True:
        print('producter %s is creating the %sth product...'%(name,count))
        time.sleep(2)
        production_queue.put(count)
        print('the %sth product has been accomplished!'%count)
        count += 1

# create a customer method
def customer(name):
    count = 1
    # eating the products
    while True:
        time.sleep(4)
        if not production_queue.empty():
            production_queue.get()
            print('customer%s is eating the %sth product...'%(name,count))
        else:
            print('there is no more product, please wait for a time...')
        count += 1

if __name__ == '__main__':
    # create a product queue
    production_queue = queue.Queue()
    p1 = threading.Thread(target=producter,args=('A',))
    c1 = threading.Thread(target=customer,args=('A',))
    c2 = threading.Thread(target=customer, args=('B',))
    c3 = threading.Thread(target=customer, args=('C',))
    p1.start()
    c1.start()
    c2.start()
    c3.start()
