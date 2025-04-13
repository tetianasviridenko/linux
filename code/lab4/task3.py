import os
import signal
import sys
import time

CONFIG_FILE = "config.txt"

def read_config(filepath):
    with open(filepath, 'r') as file:
        char = file.readline().strip()
        count = int(file.readline().strip())
    return char, count

def sighup_handler(signum, frame):
    global config_char, config_count
    config_char, config_count = read_config(CONFIG_FILE)
    print(f"Переконфігуровано: символ '{config_char}', кількість {config_count}")

def term_handler(signum, frame):
    print("Завершення роботи процесу.")
    sys.exit(0)

def child_process():
    global config_char, config_count
    config_char, config_count = read_config(CONFIG_FILE)
    signal.signal(signal.SIGHUP, sighup_handler)
    signal.signal(signal.SIGTERM, term_handler)

    print(f"Процес запущено з символом '{config_char}' і кількістю {config_count}")

    while True:
        print(f"Символ: {config_char}, Кількість: {config_count}")
        time.sleep(3)

def parent_process():
    pid = os.fork()

    if pid == 0:
        child_process()
    else:
        print(f"Запущено дочірній процес з PID: {pid}")
        sys.exit(0)

if __name__ == "__main__":
    parent_process()

