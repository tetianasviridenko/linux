import threading
import time
import random
import argparse


parser = argparse.ArgumentParser()
parser.add_argument("--buffer_size", type=int, default=5)
parser.add_argument("--duration", type=int, default=10)
parser.add_argument("--producers", type=int, default=2)
args = parser.parse_args()

buffer = []
buffer_size = args.buffer_size
buffer_lock = threading.Lock()
empty = threading.Semaphore(buffer_size)
full = threading.Semaphore(0)
stop_event = threading.Event()

def producer_thread(pid):
    while not stop_event.is_set():
        item = random.randint(1, 100)

        empty.acquire()
        with buffer_lock:
            buffer.append(item)
            print(f"[Виробник {pid}] + {item} → {buffer}")
        full.release()

        time.sleep(random.uniform(0.2, 0.5))

    print(f"[Виробник {pid}] завершив роботу.")

def consumer_thread():
    while not stop_event.is_set() or full._value > 0:
        full.acquire()
        with buffer_lock:
            if buffer:
                item = buffer.pop(0)
                print(f"[Споживач] - {item} → {buffer}")
        empty.release()

        time.sleep(random.uniform(0.3, 0.6))

    print("[Споживач] завершив роботу.")

producers = []
for i in range(args.producers):
    t = threading.Thread(target=producer_thread, args=(i+1,))
    t.start()
    producers.append(t)

consumer = threading.Thread(target=consumer_thread)
consumer.start()

time.sleep(args.duration)
print("\n[Головний потік] Час вичерпано. Зупиняємо виробників.\n")
stop_event.set()

for p in producers:
    p.join()
consumer.join()

print("\n Завершено.")
