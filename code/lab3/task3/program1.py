import os
import sys
import random

def main():
    if len(sys.argv) != 3:
        print("Використання: python program1.py <a> <b>")
        sys.exit(1)

    a = float(sys.argv[1])
    b = float(sys.argv[2])

    if not (0 <= a < b <= 1):
        print("Помилка: повинно виконуватися 0 < a < b < 1")
        sys.exit(1)

    num = int(os.getenv('NUM', 500))
    count = 0

    for _ in range(num):
        r = random.random()
        if a <= r <= b:
            count += 1

    sys.exit(min(count, 255))

if __name__ == "__main__":
    main()

