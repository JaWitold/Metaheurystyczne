import random
import os
import time
import csv


k = 1000
n_range = range(100, 1001, 100)
loops = 100
times = dict()

for n in n_range:
    print(n)
    times[n] = list()
    for loop in range(0, loops):
        command = f"C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\python.exe ..\\src\\main.py generate k-random {n} FULL_MATRIX {k} {random.randint(0, 100000)}"
        start = time.time()
        os.system(command)
        end = time.time()
        times[n].append(end - start)

print(times)
with open("test1.csv", "w") as outfile:
    writer = csv.writer(outfile)
    key_list = list(times.keys())
    writer.writerow(times.keys())
    for i in range(len(times[key_list[0]])):
        writer.writerow([times[x][i] for x in key_list])
