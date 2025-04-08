import os
import random
import time
import signal
import sys

def create_child_process():
    pid = os.fork()
    if pid == 0:
        random_number = random.random()
        if random_number >= 0.5:
            print(f"Дочірній процес {os.getpid()} завершує роботу з random_number = {random_number}")
            os._exit(0)
        else:
            print(f"Дочірній процес {os.getpid()} йде в нескінченний цикл з random_number = {random_number}")
            while True:
                time.sleep(0.1)
    return pid

def main():
    if len(sys.argv) > 1:
        num_processes = int(sys.argv[1])
    else:
        num_processes = 10

    child_pids = []

    for _ in range(num_processes):
        pid = create_child_process()
        if pid != 0:
            child_pids.append(pid)

    time.sleep(3)

    for pid in child_pids[:]:
        try:
            os.waitpid(pid, os.WNOHANG)
        except ChildProcessError:
            child_pids.remove(pid)

    print(f"Процеси-нащадки, що працюють: {child_pids}")

    time.sleep(5)

    for pid in child_pids:
        try:
            os.kill(pid, signal.SIGTERM)
            pid, exit_code = os.waitpid(pid, 0)
            if os.WIFEXITED(exit_code):
                print(f"Процес {pid} завершився нормально з кодом {os.WEXITSTATUS(exit_code)}")
            elif os.WIFSIGNALED(exit_code):
                print(f"Процес {pid} завершився через сигнал {os.WTERMSIG(exit_code)}")
            else:
                print(f"Процес {pid} завершився з невідомою причиною")
        except ProcessLookupError:
            print(f"Процес {pid} вже завершився")

if __name__ == "__main__":
    main()

