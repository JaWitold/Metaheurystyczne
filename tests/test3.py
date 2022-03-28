import random
import os
import time
import csv


# k = 1000
n_range = range(30, 101, 10)
loops = 30
times = dict()

for n in n_range:
    print(n)
    times[n] = list()
    for loop in range(0, loops):
        command = f"C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\python.exe ..\\src\\main.py generate two-opt 0, EUC_2D {n} 1000"
        start = time.time()
        os.system(command)
        end = time.time()
        times[n].append(end - start)

print(times)
with open("test3.csv", "w") as outfile:
    writer = csv.writer(outfile)
    key_list = list(times.keys())
    writer.writerow(times.keys())
    for i in range(len(times[key_list[0]])):
        writer.writerow([times[x][i] for x in key_list])
