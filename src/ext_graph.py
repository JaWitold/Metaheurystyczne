import math
import os.path
import sys

from graph import Graph


class ExtGraph(Graph):
    
    def __init__(self):
        super().__init__()
        self.best_cost = math.inf
    
    def run_all(self, algorithm, param):
        print("k-random")
        self.run("k-random", 1000)
        print("nn")
        self.run("nearest-neighbor", 1)
        # print("enn")
        # self.run("extended-nearest-neighbor", 0)
        print("2opt")
        self.run("two-opt", "1")
        
        self.save_best_cost()
    
    def prd(self, x):
        if x < self.best_cost:
            self.best_cost = x
        
    
    def save_best_cost(self):
        with open("C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\tests\\cost2.csv", "a") as outfile:
            outfile.write(f"{os.path.basename(self.filename)}, {self.best_cost} \n")
print(sys.argv)
i = ExtGraph()

i.read(sys.argv[1])
i.run_all("x", "x")
