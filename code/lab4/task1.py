import os
import sys
import time

def alarm(seconds, message):
    time.sleep(seconds)
    print(message)

def main():
    if len(sys.argv) != 3:
        print("Використання: python task1.py <секунди> <повідомлення>")
        sys.exit(1)

    try:
        interval = int(sys.argv[1])
        message = sys.argv[2]
    except ValueError:
        print("вкажіть ціле значення для секунд.")
        sys.exit(1)

    pid = os.fork()

    if pid == 0:
        alarm(interval, message)
    else:
        print(f"Будильник встановлено на {interval} секунд з повідомленням: '{message}'")
        sys.exit(0)

if __name__ == "__main__":
    main()

