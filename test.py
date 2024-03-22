from threading import Thread, Condition
import logging
from time import time, sleep


def worker(condition: Condition):
    logging.debug('Worker ready to work')
    with condition:
        condition.wait()
        timer = time()
        logging.debug('The worker can do the work')


def master(condition: Condition):
    logging.debug('Master doing some work')
    sleep(5)
    with condition:
        logging.debug('Informing that workers can do the work')
        condition.notify_all()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='%(threadName)s %(message)s')
    condition = Condition()
    master = Thread(name='master', target=master, args=(condition,))

    for i in range(10000):
        workers = Thread(name=f'worker_{i}', target=worker, args=(condition, ))
        workers.start()
    master.start()

    logging.debug('End program')