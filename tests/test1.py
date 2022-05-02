import os

main = os.getcwd()
tsp = "../vendors/ALL_tsp"
atsp = "../vendors/ALL_atsp"

fails = ''

def run(path, ending):
    # runs only on windows
    os.chdir(path)
    cwd = os.getcwd()
    
    list_of_graphs = [x for x in os.listdir(cwd) if x.endswith(ending)]
    index = 0
    
    for directory in list_of_graphs:
        index += 1
        os.chdir(directory)
        cwd = os.getcwd()
        if os.listdir(cwd)[0] == "brazil58.tsp":
            os.chdir('..')
            continue
        command = '"C:\Programs\Python 3.10.4\python.exe" ' + "C:/Dev/wppt/2022/algorytmy_metaheurystyczne/src/main.py load " + cwd + '\\' + os.listdir(cwd)[0] + " tabu 1,1,7,1"
        print(f"finnished {round(index / len(list_of_graphs) * 100)}%, ({index}/{len(list_of_graphs)})")
        result = os.system(command)
        if result != 0:
            print(command)
        os.chdir('..')
        # exit()
    
    print(list_of_graphs)


run(tsp, ".tsp")
run(atsp, ".atsp")
