import threading
import argparse

def catalan_numbers(n):
    def compute_catalan(n):
        if n <= 1:
            return 1
        res = 0
        for i in range(n):
            res += compute_catalan(i) * compute_catalan(n - 1 - i)
        return res

    catalan = []
    for i in range(n):
        catalan.append(compute_catalan(i))
    return catalan

def prime_numbers(n):
    def is_prime(num):
        if num <= 1:
            return False
        if num == 2:
            return True
        if num % 2 == 0:
            return False
        for i in range(3, int(num**0.5) + 1, 2):
            if num % i == 0:
                return False
        return True

    primes = []
    num = 2
    while len(primes) < n:
        if is_prime(num):
            primes.append(num)
        num += 1
    return primes

def main(catalan_count, prime_count):
    catalan_result = []
    prime_result = []

    def catalan_thread():
        nonlocal catalan_result
        catalan_result = catalan_numbers(catalan_count)

    def prime_thread():
        nonlocal prime_result
        prime_result = prime_numbers(prime_count)

    t1 = threading.Thread(target=catalan_thread)
    t2 = threading.Thread(target=prime_thread)

    t1.start()
    t2.start()

    t1.join()
    t2.join()

    print(f"Перші {catalan_count} чисел Каталана: {catalan_result}")
    print(f"Перші {prime_count} простих чисел: {prime_result}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обчислення чисел Каталана та простих чисел.")
    parser.add_argument("--catalan", type=int, required=True, help="Кількість чисел Каталана для обчислення")
    parser.add_argument("--primes", type=int, required=True, help="Кількість простих чисел для обчислення")

    args = parser.parse_args()

    main(args.catalan, args.primes)

