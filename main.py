import threading
import random
import time
import msvcrt

MAX_SIZE = 20
queue = []
queueIsAvailable = threading.Semaphore(5)
dataIsAvailable = threading.Semaphore(0)
mutex = threading.Lock()
endProgram = True


def producer():
    global queue
    while endProgram:
        num = random.randint(2, 5)
        queueIsAvailable.acquire()
        mutex.acquire()         # added
        print("Productor listo para trabajar")
        for i in range(num):
            if (len(queue) < MAX_SIZE):
                temp = random.randint(0, 9)
                queue.append(temp)
                print("Productor en produccion, numero producido:", temp)
                print(f"Lista con {len(queue)} espacios ocupados: ", queue)
            else:
                print("Lista llena, hablen al consumidor!!!")
                break
        mutex.release()         # added
        dataIsAvailable.release()

        print("Productor dumiendo!!")
        time.sleep(random.randint(2, 3))


def consumer():
    global queue
    while endProgram:
        num = random.randint(2, 5)
        dataIsAvailable.acquire()
        mutex.acquire()
        print("Consumidor listo para trabajar")
        for i in range(num):
            if (len(queue) != 0):
                numC = queue.pop(0)
                print("Consumo el numero:", numC)
                print(f"Lista con {len(queue)} espacios ocupados: ", queue)
            else:
                print("Ya no hay productos, llamen al productor!!!!")
                break

        mutex.release()         # added
        queueIsAvailable.release()
        print("Consumidor dumiendo!!")
        time.sleep(random.randint(5, 6))


producerThread = threading.Thread(target=producer)
consumerThread = threading.Thread(target=consumer)


producerThread.start()
consumerThread.start()

while True:
    if msvcrt.kbhit():
        leter = msvcrt.getch()
        if (leter == b'\x1b'):
            endProgram = False
            break
