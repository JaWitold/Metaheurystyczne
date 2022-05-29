import numpy as np

from graph import Graph
import copy
import math
import random
from dotenv import load_dotenv
import csv
import os



class Member:
    max_cost: int = 0
    population: Graph
    
    def __init__(self, dna):
        self.dna = dna
        self.cost = Member.population.cost(dna)
        self.normalized_cost = 0
        Member.max_cost = max(Member.max_cost, self.cost)
    
    def normalize(self, s):
        self.normalized_cost = self.cost / s


class Population(Graph):
    MAX_ITERATIONS: int = 100000
    SELECTION_RATE: float = 0.6
    MUTATION_RATE: float = 0.01
    POPULATION_MAX_SIZE: int = 128
    
    population: list[Member]
    iterations: int = 0
    
    def __init__(self):
        super().__init__()
        self.best = None
        Member.population = self
    
    def populate(self, param):
        params = [float(x) for x in param.split(",")]
        self.MAX_ITERATIONS = int(params[0])
        self.MUTATION_RATE = params[1]
        self.SELECTION_RATE = params[2]
        self.POPULATION_MAX_SIZE = int(params[3])
        
        self.population = self.generate_population()
        self.best = self.find_best(self.population)
        
        while not self.stopping_condition():
            self.iter += 1
            # Member.max_cost = max(self.population, key=lambda x: x.cost).cost
            self.population = self.selection(self.population)
            self.population = self.crossover(self.population)
            self.population = self.mutation(self.population)
            best = self.find_best(self.population)
            if best.cost < self.best.cost:
                self.best = best
                # self.prd(self.best.cost)
        
        # self.show_matrix()
        
        self.path = self.best.dna
        self.show_solution(self.best.cost)
        self.prd(self.best.cost)
    
    def run(self, algorithm, param):
        if algorithm == 'genetic':
            self.populate(param)
        elif algorithm == "k-random":
            self.k_random_method(int(param))
        elif algorithm == "nearest-neighbor":
            self.nearest_neighbor(int(param))
        elif algorithm == "two-opt":
            self.two_opt(param)
        elif algorithm == 'extended-nearest-neighbor':
            self.extended_nearest_neighbor()
        elif algorithm == 'tabu':
            self.tabu(param)
        else:
            print("Unsupported algorithm")
    
    def generate_population(self) -> list[Member]:
        population = []
        dna = np.array(range(0, self.dimension))
        for i in range(0, self.POPULATION_MAX_SIZE):
            new_dna = dna.copy()
            np.random.shuffle(new_dna)
            population.append(Member(new_dna))
        return population
    
    @staticmethod
    def find_best(population: list[Member]) -> Member:
        return min(population, key=lambda x: x.cost)
    
    def selection(self, population: list[Member]) -> list[Member]:
        """
        During each successive generation, a portion of the existing population is selected to breed a new
        generation. Individual solutions are selected through a fitness-based process, where fitter solutions (as
        measured by a fitness function) are typically more likely to be selected. Certain selection methods rate the
        fitness of each solution and preferentially select the best solutions. Other methods rate only a random
        sample of the population, as the former process may be very time-consuming.
        """
        # self.normalize(population)
        # new_population = []
        # while len(new_population) < self.POPULATION_MAX_SIZE:
        #     index = 0
        #     c = random.random()
        #     while c > 0:
        #         c -= population[index].normalized_cost
        #         index += 1
        #     index -= 1
        #     if random.random() > self.SELECTION_RATE:
        #         new_population.append(copy.deepcopy(population[index]))
        
        population = sorted(population, key=lambda x: x.cost)
        last = math.floor(len(population) * self.SELECTION_RATE)
        new_population = population[:-last] + population[: last]
        return new_population

    @staticmethod
    def normalize(population: list[Member]):
        s = sum(x.cost for x in population)
        for p in population:
            p.normalize(s)
    
    def crossover(self, population: list[Member]) -> list[Member]:
        population = sorted(population, key=lambda x: x.cost)
        new_population = []
        for t1, t2 in zip(population[::2], population[1::2]):
            c1, c2 = self.pmx(t1, t2)
            new_population.append(Member(c1))
            new_population.append(Member(c2))
        return new_population
    
    def prd(self, x):
        load_dotenv()
        ref = os.getenv(self.filename.split('\\')[-1].split('.')[0])
        if ref is None:
            print("reference value not found in .env")
            return
        ref = int(ref)
        # print(f"REF: {ref}; COST: {x}")
        result = 100 * (x - ref) / ref
        # print("PRD: {}%".format(result))
        # print(f"{self.iter}, {x}, {result}")
        with open('C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\tests\\out\\test3.csv', 'a') as fd:
            name = self.filename.split('\\')[-1]
            fd.write(f"{name}, {self.iter}, {self.MUTATION_RATE}, {self.SELECTION_RATE}, {self.POPULATION_MAX_SIZE}, "
                     f"{math.floor(x)}, {result}\n")
    
    def mutation(self, population: list[Member]) -> list[Member]:
        """
        Mutation is a genetic operator used to maintain genetic diversity from one generation of a population of
        genetic algorithm chromosomes to the next. It is analogous to biological mutation.
        """
        new_population = []
        for member in population:
            if random.random() < self.MUTATION_RATE:
                i1, i2 = np.random.choice(member.dna.shape[0], 2, replace=False)
                i1 = 0
                if i1 > i2:
                    i1, i2 = i2, i1
                # new_dna = np.copy(member.dna)
                
                new_population.append(
                    Member(
                        np.concatenate((member.dna[0:i1 + 1], member.dna[i2:i1:-1], member.dna[i2 + 1:]))
                    )
                )
            else:
                new_population.append(member)
        return new_population
    
    def pmx(self, t1, t2):
        """
        Partially mapped crossover (PMX) is one of the most popular and effective crossovers for order-based GAs
        to deal with combinatorial optimization problems, especially the TSP. In view of the operation, PMX can be
        regarded as a modification of two-point crossover but additionally uses a mapping relationship to legalize
        offspring that have duplicate numbers.
        https://www.redalyc.org/pdf/2652/265224466006.pdf
        """
        # t2 = Member(np.array([1, 2, 3, 4]))
        # t1 = Member(np.array([4, 1, 2, 3]))
        # self.dimension = 4
        crossover_point = random.randint(0, self.dimension)
        child1 = np.copy(t1.dna)
        child2 = np.copy(t1.dna)
        for i in range(0, crossover_point):
            child1[np.where(t2.dna[i] == child1)], child2[np.where(t1.dna[i] == child2)] = child1[i], child2[i]
            child1[i], child2[i] = t2.dna[i], t1.dna[i]
        
        return child1, child2


if __name__ == "__main__":
    Population.run()
