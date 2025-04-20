import os
import sys

def child_process(read_fd, write_fd):
    while True:
        message = os.read(read_fd, 1024).decode().strip()
        if message.lower() == 'stop':
            break
        upper_message = message.upper()
        os.write(write_fd, upper_message.encode())
    os.close(read_fd)
    os.close(write_fd)
    sys.exit(0)

def main():
    parent_read_fd, child_write_fd = os.pipe()
    child_read_fd, parent_write_fd = os.pipe()

    pid = os.fork()

    if pid == 0:
        os.close(parent_read_fd)
        os.close(parent_write_fd)
        child_process(child_read_fd, child_write_fd)
    else:
        os.close(child_read_fd)
        os.close(child_write_fd)

        while True:
            message = input("Введіть текст (або 'stop' для завершення): ").strip()
            os.write(parent_write_fd, message.encode())

            if message.lower() == 'stop':
                break
            upper_message = os.read(parent_read_fd, 1024).decode().strip()
            print(f"Отримано від дочірнього процесу: {upper_message}")
        os.close(parent_read_fd)
        os.close(parent_write_fd)
        os.wait()

if __name__ == "__main__":
    main()
