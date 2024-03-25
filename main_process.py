import time
from multiprocessing import Process, Queue,


def factorize_number(num, output=None):
    """Function calculates the factorial"""
    factors = []
    for i in range(1, num + 1):
        if num % i == 0:
            factors.append(i)

    if output is None:
        return factors
    else:
        output.put(factors)

def factorize_sync(*number):
    """Synchronous factorial calculation function"""
    timer = time.time()
    factors_list = []
    for num in number:
        factors_list.append(factorize_number(num))

    print(f"Sync version: {time.time() - timer}")
    return factors_list

def factorize_process(*number):
    """Multi-processor factorial calculation function"""
    timer = time.time()
    output = Queue()

    factors_list = []
    process_list = []
    for num in number:
        pr = Process(target=factorize_number, args=(num, output))
        pr.start()
        process_list.append(pr)

    [el.join() for el in process_list]

    while not output.empty():
        factors_list.extend([output.get()])

    #print(factors_list)
    print(f"Multi-processor version: {time.time() - timer}")
    return factors_list

if __name__ == '__main__':

    a, b, c, d  = factorize_sync(128, 255, 99999, 10651060)

    a, b, c, d  = factorize_process(128, 255, 99999, 10651060)

    assert a == [1, 2, 4, 8, 16, 32, 64, 128]
    assert b == [1, 3, 5, 15, 17, 51, 85, 255]
    assert c == [1, 3, 9, 41, 123, 271, 369, 813, 2439, 11111, 33333, 99999]
    assert d == [1, 2, 4, 5, 7, 10, 14, 20, 28, 35, 70, 140, 76079, 152158, 304316, 380395, 532553, 760790, 1065106, 1521580, 2130212, 2662765, 5325530, 10651060]