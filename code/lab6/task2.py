import mmap
import pickle
import os
import random
import string
import fcntl

MESSAGE_SIZE = 100
NUM_CHILDREN = 5

def create_shared_memory():
    file_name = 'shared_memory.dat'
    with open(file_name, 'wb') as f:
        f.write(b'\x00' * (MESSAGE_SIZE * NUM_CHILDREN))
    
    file = open(file_name, 'r+b')
    mmap_obj = mmap.mmap(file.fileno(), 0)
    return file, mmap_obj

def serialize_message(index):
    message = ''.join(random.choices(string.ascii_letters + string.digits, k=50))
    serialized_message = pickle.dumps(message)

    if len(serialized_message) > MESSAGE_SIZE:
        raise ValueError(f"Серійоване повідомлення занадто велике. Розмір: {len(serialized_message)}")

    return serialized_message

def write_to_shared_memory(file, mmap_obj, index):
    serialized_message = serialize_message(index)

    fcntl.lockf(file, fcntl.LOCK_EX, MESSAGE_SIZE * index, MESSAGE_SIZE)

    mmap_obj[MESSAGE_SIZE * index:MESSAGE_SIZE * (index + 1)] = serialized_message.ljust(MESSAGE_SIZE)
    print(f"Процес {os.getpid()} завершив запис в індекс {index + 1}.")

    fcntl.lockf(file, fcntl.LOCK_UN, MESSAGE_SIZE * index, MESSAGE_SIZE)

def read_from_shared_memory(file, mmap_obj):
    for i in range(NUM_CHILDREN):
        fcntl.lockf(file, fcntl.LOCK_SH, MESSAGE_SIZE * i, MESSAGE_SIZE)
        
        serialized_message = mmap_obj[MESSAGE_SIZE * i:MESSAGE_SIZE * (i + 1)].rstrip(b'\x00')

        try:
            message = pickle.loads(serialized_message)
            print(f"Прочитано повідомлення {i + 1}: {message}")
        except EOFError:
            print(f"Порожні дані в індексі {i + 1}")

        fcntl.lockf(file, fcntl.LOCK_UN, MESSAGE_SIZE * i, MESSAGE_SIZE)

def main():
    file, mmap_obj = create_shared_memory()

    for i in range(NUM_CHILDREN):
        pid = os.fork()
        
        if pid == 0:
            write_to_shared_memory(file, mmap_obj, i)
            os._exit(0)

    for _ in range(NUM_CHILDREN):
        os.wait()

    read_from_shared_memory(file, mmap_obj)

    mmap_obj.close()
    file.close()

if __name__ == "__main__":
    main()

