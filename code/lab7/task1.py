import os
import threading
import time

class MyLock:
    def __init__(self):
        self.read_fd, self.write_fd = os.pipe()

    def acquire(self):
        os.read(self.read_fd, 1)

    def release(self):
        os.write(self.write_fd, b'x')

    def __del__(self):
        os.close(self.read_fd)
        os.close(self.write_fd)

def worker(lock, thread_id):
    print(f"Потік {thread_id} очікує на отримання блокування")    
    lock.acquire()
    print(f"Потік {thread_id} отримав блокування")    
    time.sleep(2)
    print(f"Потік {thread_id} звільняє блокування")   
    lock.release()

if __name__ == "__main__":
    lock = MyLock()

    threads = []
    for i in range(2):
        t = threading.Thread(target=worker, args=(lock, i))
        threads.append(t)
        t.start()

    time.sleep(1)

    lock.release()
    lock.release()

    for t in threads:
        t.join()

    print("Всі потоки завершили роботу")
