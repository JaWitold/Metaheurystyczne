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
        if os.listdir(cwd)[0] == "berlin52.tsp":
            for p in range(10, 11, 10):
                for i in range(10000, 10001, 1000):
                    for m in range(5, 96, 10):
                        for n in range(0, 3):
                            command = '"C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\python.exe" ' + "C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\src\\main.py load " + cwd + '\\' + \
                                      os.listdir(cwd)[0] + f" genetic {i},{m / 100},0.95,{p}"
                            os.system(command)
        os.chdir('..')
        # exit()
    
    print(list_of_graphs)


run(tsp, ".tsp")
# run(atsp, ".atsp")
