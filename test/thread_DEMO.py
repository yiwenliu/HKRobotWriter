import threading
import multiprocessing
if __name__ == '__main__':
    print 'thread %s is running' % (threading.current_thread().name)
    print multiprocessing.cpu_count()