from matplotlib import pyplot as plt
import sys
import random
import copy
import os
from dotenv import load_dotenv

from generate import GraphGenerator


class Graph:
    supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
    supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']
    
    supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']
    
    edge_weight_format = ""
    filename = ""
    
    header = dict()
    dimension = 0
    matrix = []
    coordinates = dict()
    path = []
    
    def __init__(self):
        self.read_data_from = {
            "FULL_MATRIX": self.read_data_from_full_matrix,
            "EUC_2D": self.read_data_from_euc_2d,
            "LOWER_DIAG_ROW": self.read_data_from_lower_diag_row
        }
    
    def generate(self, variant, dimension, seed, upper_bound=100):
        generator = GraphGenerator(variant, dimension, seed, upper_bound)
        self.matrix,self.coordinates = generator.generate()
        self.dimension = len(self.matrix)
        self.edge_weight_format = variant
    
    def read(self, filename):
        self.filename = filename
        with open(self.filename, 'r') as file:
            for line in file:
                line = line.replace(":", "")
                if any(x in line for x in self.supported_header_delimiters):
                    break
                split = [x.strip() for x in line.split(maxsplit=1)]
                if len(split) < 2:
                    break
                key, value = split
                self.header[key] = value
            
            self.set_edge_weight_format()
            self.set_dimension()
            
            if self.edge_weight_format not in self.supported_formats:
                print("Unsupported data format")
                exit(1)
            
            self.matrix = [[0 for y in range(0, self.dimension)] for x in range(0, self.dimension)]
            self.read_data_from[self.edge_weight_format](file)
    
    def set_edge_weight_format(self):
        for format_key in self.supported_format_keys:
            if format_key in self.header.keys():
                self.edge_weight_format = self.header[format_key]
                break
    
    def set_dimension(self):
        self.dimension = int(self.header["DIMENSION"])
        self.path = [x for x in range(0, self.dimension)]
    
    def read_data_from_full_matrix(self, file):
        numbers = self.read_numbers(file)
        for i in range(0, self.dimension):
            for j in range(0, self.dimension):
                self.matrix[i][j] = int(numbers[i * self.dimension + j])
    
    def read_data_from_lower_diag_row(self, file):
        numbers = self.read_numbers(file)
        index = 0
        for i in range(0, self.dimension):
            for j in range(0, i + 1):
                self.matrix[i][j] = self.matrix[j][i] = numbers[index]
                index += 1
    
    def read_data_from_euc_2d(self, file):
        numbers = [a for a in [x.split() for x in file.readlines()] if len(a) == 3]
        index = 0
        for i in range(0, self.dimension):
            ni, ni_x, ni_y = numbers[i]
            self.coordinates[int(ni)] = {'x': int(float(ni_x)), 'y': int(float(ni_y))}
            for j in range(0, i + 1):
                nj, nj_x, nj_y = numbers[j]
                distance = int(((float(ni_x) - float(nj_x)) ** 2 + (float(ni_y) - float(nj_y)) ** 2) ** 0.5)
                self.matrix[i][j] = self.matrix[j][i] = distance
                index += 1
    
    def show_matrix(self):
        for subset in self.matrix:
            print(subset)
        self.draw()
    
    def draw(self):
        if self.edge_weight_format == 'EUC_2D':
            # draw lines
            for i in range(0, self.dimension):
                ni = self.coordinates[i + 1]
                for j in range(0, i):
                    nj = self.coordinates[j + 1]
                    plt.plot([ni['x'], nj['x']], [ni['y'], nj['y']], color="red", linewidth=0.1)
            # draw points
            for node in self.coordinates.values():
                plt.plot(node['x'], node['y'], color="blue", marker="o", markersize=2)
            plt.show()
    
    def k_random_method(self, k):
        min_dist = sys.maxsize
        vertex = [x for x in range(self.dimension)]
        path = []
        for j in range(k):
            random.shuffle(vertex)
            distance = self.cost(vertex)
            if distance < min_dist:
                min_dist = distance
                path = vertex.copy()
        self.path = path
        cost = min_dist
        # self.show_matrix()
        # self.show_solution(cost)
        # self.draw_solution()
        # self.prd(cost)
    
    def nearest_neighbor(self, start):
        #self.show_matrix()
        min_dist=0
        path = [start]
        matrix_copy=copy.deepcopy(self.matrix)
        indexes=[x for x in range(self.dimension)]
        while(len(path)!=self.dimension):
            points=dict(zip(indexes,matrix_copy[start]))
            neighbors=sorted(points.items(), key=lambda x: x[1])
            for key,value in neighbors:
                if key not in path:
                    start=key
                    min_dist = min_dist + int(value)
                    path.append(key)
                    break
        min_dist = min_dist + int(self.matrix[path[0]][path[self.dimension-1]])
        # self.path = path
        # self.show_matrix()
        # self.show_solution(min_dist)
        # self.draw_solution()
        self.prd(min_dist)
    
    #oduzaleznienie od wyboru sasiada poprzez sprawdzenie trasy dla kazdego wierzc
    def extended_nearest_neighbor(self):
        min_dist_total=sys.maxsize
        starting_vertex=-1
        path_total=[]
        for start in range(self.dimension):
            vertex=start
            min_dist=0
            path = [start]
            matrix_copy=copy.deepcopy(self.matrix)
            indexes=[x for x in range(self.dimension)]
            while(len(path)!=self.dimension):
                points=dict(zip(indexes,matrix_copy[start]))
                neighbors=sorted(points.items(), key=lambda x: x[1])
                for key,value in neighbors:
                    if key not in path:
                        start=key
                        min_dist = min_dist + int(value)
                        path.append(key)
                        break
            min_dist = min_dist + int(self.matrix[path[0]][path[self.dimension-1]])
            if(min_dist_total>min_dist):
                min_dist_total=min_dist
                starting_vertex=vertex
                path_total=copy.deepcopy(path)
        pass
        self.path=path_total
        # self.show_matrix()
        # print("Best start: ", starting_vertex)
        # self.show_solution(min_dist_total)
        # self.draw_solution()
        self.prd(min_dist_total)
    
    # Cost function
    def cost(self, path):
        distance = 0
        for i in range(len(path)):
            if i + 1 == len(path):
                distance = distance + int(self.matrix[path[i]][path[0]])
                break
            distance = distance + int(self.matrix[path[i]][path[i + 1]])
        return distance
    
    def two_opt(self, param):
        path = [x for x in range(self.dimension)]
        #path = [int(x) for x in param.split(",")]
        if len(path) != self.dimension:
            print(f"path is too short, expected {self.dimension}")
            return
        best = path
        improved = True
        while improved:
            improved = False
            for i in range(0, len(path) - 1):
                for j in range(i + 1, len(path)):
                    # if j - i == 1: continue
                    current_cost=self.cost(best)
                    new_route = path[:]
                    new_route[i:j] = reversed(new_route[i:j])
                    if self.cost(new_route) < current_cost:
                        best = new_route
                        improved = True
            path = best
        self.path = path
        cost = self.cost(self.path)
        # self.show_matrix()
        # self.show_solution(cost)
        # self.draw_solution()
        self.prd(cost)
    
    def show_solution(self, cost):
        print(f"Cost: {cost}")
        print(f"Path: {self.path}")
    
    def draw_solution(self):
        if self.edge_weight_format == 'EUC_2D':
            for i in range(0, len(self.path)):
                ni = self.coordinates[self.path[i] + 1]
                nj = self.coordinates[self.path[(i + 1) % len(self.path)] + 1]
                plt.plot([ni['x'], nj['x']], [ni['y'], nj['y']], color="red", linewidth=0.2)
            for node in self.coordinates.values():
                plt.plot(node['x'], node['y'], color="blue", marker="o", markersize=2)
            plt.show()
    
    def prd(self, x):
        load_dotenv()
        ref = os.getenv(os.path.basename(self.filename))
        if ref is None:
            print("reference value not found in .env")
            return
        ref = int(ref)
        print(f"reference value: {ref}")
        result = 100 * (x - ref) / ref
        print("PRD(x):{}%".format(result))
    
    @staticmethod
    def read_numbers(file):
        return [item for sublist in [x.split() for x in file.readlines()] for item in sublist if
                item.isnumeric()]
    
    def run(self, algorithm, param):
        if algorithm == "k-random":
            self.k_random_method(int(param))
        elif algorithm == "nearest-neighbor":
            self.nearest_neighbor(int(param))
        elif algorithm == "two-opt":
            self.two_opt(param)
        elif algorithm == 'extended-nearest-neighbor':
            self.extended_nearest_neighbor()
        else:
            print("Unsupported algorithm")
