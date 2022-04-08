import math
import os.path
import sys

from graph import Graph


class ExtGraph(Graph):
    def __init__(self):
        super().__init__()
        self.best_cost = math.inf
    
    def run_all(self, algorithm, param):
        print("2opt")
        self.run("two-opt", "1")
        
        self.save_best_cost()
    
    def prd(self, x):
        if x < self.best_cost:
            self.best_cost = x
        
    
    def save_best_cost(self):
        with open("C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\tests\\best_cost_tsp.csv", "a") as outfile:
            outfile.write(f"{os.path.basename(self.filename)}, {self.best_cost} \n")
# print(sys.argv)
# i = ExtGraph()
#
# i.read("C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\vendors\\ALL_tsp\\kroA100.tsp\\kroA100.tsp")
# i.run_all("x", "x")
