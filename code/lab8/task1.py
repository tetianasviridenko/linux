import threading
import math
import time

def integrate_single_thread(func, a, b, n):
    h = (b - a) / n
    integral_sum = 0
    for i in range(n):
        midpoint = a + (i + 0.5) * h
        integral_sum += func(midpoint)
    return integral_sum * h

def integrate(func, a, b, eps=1e-6, max_iterations=100):
    n = 10
    prev_integral = integrate_single_thread(func, a, b, n)
    for _ in range(max_iterations):
        n *= 2
        current_integral = integrate_single_thread(func, a, b, n)
        if abs(current_integral - prev_integral) <= eps:
            return current_integral
        prev_integral = current_integral
    return current_integral

def worker(func, a_part, b_part, results, index, eps):
    results[index] = integrate(func, a_part, b_part, eps)

def parallel_integrate(func, a, b, eps=1e-6, num_threads=4):
    if num_threads <= 1:
        return integrate(func, a, b, eps)

    segment_length = (b - a) / num_threads
    threads = []
    results = [0] * num_threads

    for i in range(num_threads):
        start = a + i * segment_length
        end = a + (i + 1) * segment_length
        thread = threading.Thread(target=worker, args=(func, start, end, results, i, eps / num_threads))
        threads.append(thread)
        thread.start()

    for thread in threads:
        thread.join()

    return sum(results)

if __name__ == '__main__':
    def my_function(x):
        return x**2 

    lower_bound = 0
    upper_bound = 2
    tolerance = 1e-7
    num_threads_to_use = 4

    start_time_single = time.time()
    result_single = integrate(my_function, lower_bound, upper_bound, tolerance)
    time_single = time.time() - start_time_single

    print(f"[Однопоток] Результат: {result_single:.8f}, Час: {time_single:.6f} сек")

    start_time_parallel = time.time()
    result_parallel = parallel_integrate(my_function, lower_bound, upper_bound, tolerance, num_threads_to_use)
    time_parallel = time.time() - start_time_parallel

    print(f"[Багатопоток] Результат: {result_parallel:.8f}, Час: {time_parallel:.6f} сек")

    exact_value = 8 / 3
    print(f"[Очікуване] Точне значення: {exact_value:.8f}")

