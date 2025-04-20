import os

FIFO_TO_CHILD = '/tmp/fifo_to_child'
FIFO_TO_PARENT = '/tmp/fifo_to_parent'

def main():
    try:
        os.mkfifo(FIFO_TO_CHILD)
        os.mkfifo(FIFO_TO_PARENT)
    except FileExistsError:
        pass

    pid = os.fork()

    if pid != 0:
        with open(FIFO_TO_CHILD, 'w') as fifo_to_child, open(FIFO_TO_PARENT, 'r') as fifo_to_parent:
            while True:
                message = input("Введіть текст (або 'stop' для завершення): ").strip()
                fifo_to_child.write(message + '\n')
                fifo_to_child.flush()

                if message.lower() == 'stop':
                    break

                upper_message = fifo_to_parent.readline().strip()
                print(f"Отримано від дочірнього процесу: {upper_message}")

        os.remove(FIFO_TO_CHILD)
        os.remove(FIFO_TO_PARENT)

    elif pid == 0:
        with open(FIFO_TO_CHILD, 'r') as fifo_to_child, open(FIFO_TO_PARENT, 'w') as fifo_to_parent:
            while True:
                message = fifo_to_child.readline().strip()
                if message.lower() == 'stop':
                    break

                upper_message = message.upper()
                fifo_to_parent.write(upper_message + '\n')
                fifo_to_parent.flush()

if __name__ == "__main__":
    main()
