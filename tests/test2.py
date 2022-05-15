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
    r = range(100, 1001, 100)
    for directory in list_of_graphs:
        index += 1
        os.chdir(directory)
        cwd = os.getcwd()
        if os.listdir(cwd)[0] == "brazil58.tsp":
            os.chdir('..')
            continue
        print(os.listdir(cwd)[0])
        for i in r:
            index += 1
            command = '" C:\\Users\\user\\AppData\\Local\\Programs\\Python\\Python39\\python.exe" ' + "C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\src\\main.py load " + f"C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\vendors\\ALL_tsp\\{os.listdir(cwd)[0]}\\{os.listdir(cwd)[0]}" + f" tabu {i},200,50,20"
            print(f"finnished {round(index / (len(r) * len(list_of_graphs)) * 100)}%, ({index}/{len(r) * len(list_of_graphs)})")
            result = os.system(command)
            if result != 0:
                print(command)
        os.chdir('..')
        # exit()


run(tsp, ".tsp")
# run(atsp, ".atsp")
