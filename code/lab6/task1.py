import os
import mmap
import fcntl
import pickle
import random
import string

def generate_random_string(length):
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for _ in range(length))

def child_process(lock_file_path, mmap_obj):
    random_string = generate_random_string(random.randint(5, 20))
    message = {'pid': os.getpid(), 'str': random_string}
    serialized_message = pickle.dumps(message)
    message_length = len(serialized_message)

    with open(lock_file_path, 'r+') as lock_file:
        fcntl.flock(lock_file, fcntl.LOCK_EX)
        try:
            size = int.from_bytes(mmap_obj[:4], byteorder='big')

            mmap_obj[4 + size: 4 + size + 4] = message_length.to_bytes(4, byteorder='big')
            mmap_obj[4 + size + 4: 4 + size + 4 + message_length] = serialized_message

            new_size = size + 4 + message_length
            mmap_obj[:4] = new_size.to_bytes(4, byteorder='big')
        finally:
            fcntl.flock(lock_file, fcntl.LOCK_UN)

    os._exit(0)

def parent_process(lock_file_path, mmap_obj, num_children):
    print("Очікування завершення дочірніх процесів...")

    for _ in range(num_children):
        os.wait()

    print("Усі дочірні процеси завершено.")
    print("Читання даних зі спільної пам'яті...")

    size = int.from_bytes(mmap_obj[:4], byteorder='big')
    offset = 0
    messages = []

    while offset < size:
        message_length = int.from_bytes(mmap_obj[4 + offset : 4 + offset + 4], byteorder='big')
        offset += 4
        message_data = mmap_obj[4 + offset : 4 + offset + message_length]
        message = pickle.loads(message_data)
        messages.append(message)
        offset += message_length

    print("Отримані повідомлення:")
    for msg in messages:
        print(f"Отримано від PID {msg['pid']}: {msg['str']}")

def main():
    lock_file_path = 'lockfile'
    num_children = 5
    mmap_size = 4096

    print("Створення файлу для блокування...")
    open(lock_file_path, 'w').close()

    print("Створення анонімного сегменту пам'яті...")
    mmap_obj = mmap.mmap(-1, mmap_size)
    mmap_obj[:4] = (0).to_bytes(4, byteorder='big')

    print(f"Створення {num_children} дочірніх процесів...")
    for _ in range(num_children):
        pid = os.fork()
        if pid == 0:
            child_process(lock_file_path, mmap_obj)

    parent_process(lock_file_path, mmap_obj, num_children)

    print("Закриття відображення пам'яті та видалення файлу блокування...")
    mmap_obj.close()
    os.remove(lock_file_path)
    print("Роботу завершено.")

if __name__ == '__main__':
    main()

