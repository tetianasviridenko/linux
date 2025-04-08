import os
import sys

def main():
    if len(sys.argv) != 3:
        print("Використання: python program0.py <n> <num>")
        sys.exit(1)

    n = int(sys.argv[1])
    num = int(sys.argv[2])

    if n <= 0 or num <= 0:
        print("Помилка: n та num мають бути додатними цілими числами")
        sys.exit(1)

    os.environ['NUM'] = str(num)
    interval_size = 1.0 / n

    results = []

    for i in range(n):
        a = i * interval_size
        b = (i + 1) * interval_size
        pid = os.fork()

        if pid == 0:
            os.execlp("python", "python", "program1.py", str(a), str(b))
        else:
            _, status = os.waitpid(pid, 0)
            result = os.WEXITSTATUS(status)
            results.append(result)

    for i, result in enumerate(results):
        print(f"Процес {i + 1} повернув значення {result}")

if __name__ == "__main__":
    main()


