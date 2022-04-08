import os
import time

start = time.time()
main = os.getcwd()
tsp = "..\\vendors\\ALL_tsp"
atsp = "..\\vendors\\ALL_atsp"

current = os.getcwd()


def run(path, ending):
    # runs only on Windows
    os.chdir(path)
    cwd = os.getcwd()
    
    dictionaries = [x for x in os.listdir(cwd) if x.endswith(ending)]
    dictionaries.sort()
    index = 0
    
    for directory in dictionaries:
        index += 1
        os.chdir(directory)
        cwd = os.getcwd()
        command = f"C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\python.exe {current}\\ext_graph.py {current}\\{path}\\{os.listdir(cwd)[0]}\\{os.listdir(cwd)[0]} "
        print(command)
        print(f"finished {round(index / len(dictionaries) * 100)}%, ({index}/{len(dictionaries)})")
        os.system(command)
        os.chdir('..')
    
    print(dictionaries)


# run(tsp, ".tsp")
# os.chdir(current)
run(atsp, ".atsp")
stop = time.time()
print(stop - start)
