import timeit
import random
import csv
import statistics
import psutil
import os
import matplotlib.pyplot as plt

def quicksort(arr):
    if len(arr) <= 1:
        return arr
    pivot = arr[len(arr) // 2]
    left = [x for x in arr if x < pivot]
    middle = [x for x in arr if x == pivot]
    right = [x for x in arr if x > pivot]
    return quicksort(left) + middle + quicksort(right)

def generate_random_list(size):
    return [random.randint(1, 100) for _ in range(size)]

results = []

# Ustawienie procesu do pomiaru pamięci
process = psutil.Process(os.getpid())

# Zbiory do przechowywania wartości CPU i pamięci
cpu_usages = []
memory_usages = []

# Perform the test 100 times with random list sizes between 10 and 10000
for _ in range(100):
    size = random.randint(10, 10000)
    arr = generate_random_list(size)

    # Measure CPU and memory usage before sorting
    cpu_before = psutil.cpu_percent(interval=0.1)  # Krótkie odstępy dla stabilności
    memory_before = process.memory_info().rss  # Zużycie pamięci przez aktualny proces

    # Measure time to sort using quicksort
    time = timeit.timeit(lambda: quicksort(arr.copy()), number=1)

    # Measure CPU and memory usage after sorting
    cpu_after = psutil.cpu_percent(interval=0.1)
    memory_after = process.memory_info().rss

    # Obliczanie zużycia CPU i pamięci
    cpu_usage = max(0, cpu_after - cpu_before)  # CPU nie powinno być ujemne
    memory_usage = max(0, memory_after - memory_before)  # Pamięć nie powinna być ujemna

    results.append((size, time, cpu_usage, memory_usage))

    cpu_usages.append(cpu_usage)
    memory_usages.append(memory_usage)

    print(f"Czas do posortowania tablicy {size} elementów: {time:.6f} sekund, CPU: {cpu_usage:.2f}%, Pamięć: {memory_usage / (1024 * 1024):.2f} MB")

# Save results to a CSV file
with open('results.csv', 'w', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Size', 'Time', 'CPU Usage (%)', 'Memory Usage (MB)'])
    writer.writerows([(size, time, cpu, mem / (1024 * 1024)) for size, time, cpu, mem in results])

# Calculate and print average and standard deviation for time
times = [result[1] for result in results]
average_time = statistics.mean(times)
std_dev_time = statistics.stdev(times)

print(f"Średni czas sortowania: {average_time:.6f} sekund")
print(f"Odchylenie standardowe czasu sortowania: {std_dev_time:.6f} sekund")

# Calculate and print average and standard deviation for CPU usage
average_cpu = statistics.mean(cpu_usages)
std_dev_cpu = statistics.stdev(cpu_usages)

print(f"Średnie obciążenie CPU: {average_cpu:.2f}%")
print(f"Odchylenie standardowe obciążenia CPU: {std_dev_cpu:.2f}%")

# Calculate and print average and standard deviation for memory usage
average_memory = statistics.mean(memory_usages)
std_dev_memory = statistics.stdev(memory_usages)

print(f"Średnie zużycie pamięci: {average_memory / (1024 * 1024):.2f} MB")
print(f"Odchylenie standardowe zużycia pamięci: {std_dev_memory / (1024 * 1024):.2f} MB")

# Plot the data using matplotlib
sizes = [result[0] for result in results]
times = [result[1] for result in results]
cpu_usages = [result[2] for result in results]
memory_usages = [result[3] / (1024 * 1024) for result in results]  # Convert memory usage to MB

# Plot Time vs Size
plt.figure(figsize=(10, 6))
plt.subplot(2, 2, 1)
plt.plot(sizes, times, marker='o', color='b', label="Czas sortowania")
plt.xlabel('Rozmiar tablicy')
plt.ylabel('Czas (sekundy)')
plt.title('Czas sortowania vs Rozmiar tablicy')
plt.grid(True)

# Plot CPU Usage vs Size
plt.subplot(2, 2, 2)
plt.plot(sizes, cpu_usages, marker='o', color='g', label="Obciążenie CPU")
plt.xlabel('Rozmiar tablicy')
plt.ylabel('Obciążenie CPU (%)')
plt.title('Obciążenie CPU vs Rozmiar tablicy')
plt.grid(True)

# Plot Memory Usage vs Size
plt.subplot(2, 2, 3)
plt.plot(sizes, memory_usages, marker='o', color='r', label="Zużycie pamięci")
plt.xlabel('Rozmiar tablicy')
plt.ylabel('Zużycie pamięci (MB)')
plt.title('Zużycie pamięci vs Rozmiar tablicy')
plt.grid(True)

# Adjust layout to avoid overlap
plt.tight_layout()

# Show the plots
plt.show()
