import os
import signal
import sys
import time
sigusr1_count = 0
sigusr2_count = 0

def sigusr1_handler(signum, frame):
    global sigusr1_count
    sigusr1_count += 1
def sigusr2_handler(signum, frame):
    global sigusr2_count
    sigusr2_count += 1
def term_handler(signum, frame):
    print(f"Отримано SIGUSR1: {sigusr1_count}")
    print(f"Отримано SIGUSR2 (імітація SIGRTMIN): {sigusr2_count}")
    sys.exit(0)

def child_process():
    global sigusr1_count, sigusr2_count
    signal.signal(signal.SIGUSR1, sigusr1_handler)
    signal.signal(signal.SIGUSR2, sigusr2_handler)
    signal.signal(signal.SIGTERM, term_handler)
    signal.pthread_sigmask(signal.SIG_BLOCK, [signal.SIGUSR1, signal.SIGUSR2])
    os.kill(os.getppid(), signal.SIGALRM)

    signal.pthread_sigmask(signal.SIG_UNBLOCK, [signal.SIGUSR1, signal.SIGUSR2])

    while True:
        signal.pause()
def parent_process(num_signals):
    pid = os.fork()

    if pid == 0:
        child_process()
    else:
        signal.signal(signal.SIGALRM, lambda s, f: None)
        signal.pause()
        for _ in range(num_signals):
            os.kill(pid, signal.SIGUSR1)
            os.kill(pid, signal.SIGUSR2)
        time.sleep(1)

        os.kill(pid, signal.SIGTERM)
        os.wait()
        print("Дочірній процес завершено.")
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Використання: python3 task2.py <кількість_сигналів>")
        sys.exit(1)

    try:
        num_signals = int(sys.argv[1])
    except ValueError:
        print("Невірне значення кількості сигналів. Вкажіть ціле число.")
        sys.exit(1)
    parent_process(num_signals)
