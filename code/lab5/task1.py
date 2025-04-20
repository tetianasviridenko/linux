import os
import time
import sys
def child_process(write_fd):

    print(f"Дочірній процес (PID: {os.getpid()}) працює")
    time.sleep(2)
    print(f"Дочірній процес (PID: {os.getpid()}) завершив роботу")

    os.write(write_fd, b"done\n")

    os.close(write_fd)
    sys.exit(0)

def main(n):
    read_fd, write_fd = os.pipe()

    for i in range(n):
        pid = os.fork()

        if pid == 0:
            os.close(read_fd)
            child_process(write_fd)

    os.close(write_fd)

    for i in range(n):
        signal = os.read(read_fd, 5)
        print(f"Батьківський процес отримав сигнал від дочірнього процесу {i + 1}")
    os.close(read_fd)
    print(f"Батьківський процес (PID: {os.getpid()}) продовжує свою роботу")

    for i in range(n):
        os.wait()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print(f"Використання: {sys.argv[0]} <кількість_дочірніх_процесів>")
        sys.exit(1)

    n = int(sys.argv[1])
    main(n)

