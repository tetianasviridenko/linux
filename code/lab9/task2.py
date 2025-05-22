import threading
import time
import random
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--duration', type=int, default=10, help='Тривалість роботи (секунди)')
parser.add_argument('--buffer_size', type=int, default=3, help='Розмір буфера')
parser.add_argument('--producers', type=int, default=2, help='Кількість потоків-виробників')
args = parser.parse_args()

storage = []
buffer_limit = args.buffer_size
storage_lock = threading.Lock()
storage_cond = threading.Condition(lock=storage_lock)

stop_event = threading.Event()

def producer(pid):
    while not stop_event.is_set():
        item = random.randint(100, 999)

        with storage_cond:
            while len(storage) >= buffer_limit:
                storage_cond.wait()
            storage.append(item)
            print(f"[Виробник {pid}] Створено: {item} → Буфер: {storage}")
            storage_cond.notify_all()

        time.sleep(random.uniform(0.2, 0.5))

    print(f"[Виробник {pid}] Завершує роботу.")

def consumer():
    while not stop_event.is_set() or storage:
        with storage_cond:
            while not storage:
                if stop_event.is_set():
                    return
                storage_cond.wait()
            item = storage.pop(0)
            print(f"[Споживач] Отримано: {item} → Буфер: {storage}")
            storage_cond.notify_all()

        time.sleep(random.uniform(0.3, 0.6))

    print("[Споживач] Завершує роботу.")

producer_threads = []
for i in range(args.producers):
    t = threading.Thread(target=producer, args=(i+1,))
    t.start()
    producer_threads.append(t)

consumer_thread = threading.Thread(target=consumer)
consumer_thread.start()

time.sleep(args.duration)
print("\n[Головний потік] Час вичерпано. Завершуємо виробників.\n")
stop_event.set()

with storage_cond:
    storage_cond.notify_all()

for t in producer_threads:
    t.join()
consumer_thread.join()

print("\n Програма завершена.")


