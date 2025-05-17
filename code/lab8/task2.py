import threading
import time
import random
from datetime import datetime

class Task:
    def __init__(self, priority):
        self.priority = priority

    def execute(self, thread_id):
        start_time = datetime.now()
        print(f"[{start_time.strftime('%H:%M:%S')}] Потік {thread_id} почав завдання з пріоритетом {self.priority}")
        
        time.sleep(random.uniform(0.1, 0.5))

        end_time = datetime.now()
        print(f"[{end_time.strftime('%H:%M:%S')}] Потік {thread_id} завершив завдання з пріоритетом {self.priority}")

class TaskQueue:
    def __init__(self):
        self.tasks = []
        self.lock = threading.Lock()

    def add_task(self, task):
        with self.lock:
            self.tasks.append(task)
            self.tasks.sort(key=lambda x: x.priority, reverse=True)

    def get_task(self):
        with self.lock:
            if self.tasks:
                return self.tasks.pop(0)
            return None

def worker(queue, thread_id):
    while True:
        task = queue.get_task()
        if task is None:
            break
        task.execute(thread_id)

def main():
    task_queue = TaskQueue()

    for i in range(10):
        task_queue.add_task(Task(random.randint(1, 10)))

    start_time = datetime.now()
    print(f"\nПочаток виконання: {start_time.strftime('%H:%M:%S')}\n")

    threads = []
    for i in range(3):
        thread = threading.Thread(target=worker, args=(task_queue, i))
        thread.start()
        threads.append(thread)

    for thread in threads:
        thread.join()

    end_time = datetime.now()
    print(f"\nЗавершення виконання: {end_time.strftime('%H:%M:%S')}")

    duration = end_time - start_time
    minutes, seconds = divmod(duration.total_seconds(), 60)
    print(f"Загальний час виконання: {int(minutes)} хв {int(seconds)} сек\n")

if __name__ == "__main__":
    main()

