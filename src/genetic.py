from graph import Graph
import math
import random


class Member:
    max_cost: int = 0
    
    def __init__(self, dna: list[int]):
        self.dna = dna
        self.cost = 0
        self.normalized_cost = 0
    
    def set_cost(self, cost: int):
        self.cost = cost
        if cost > self.max_cost:
            self.max_cost = cost
    
    def normalize(self):
        self.normalized_cost = self.cost / self.max_cost


class Population(Graph):
    MAX_ITERATIONS: int = 100000
    SELECTION_RATE: float = 0.6
    MUTATION_RATE: float = 0.01
    
    population: list[Member] = []
    iterations: int = 0
    
    def __init__(self):
        super().__init__()
        self.populationMaxSize = 128
    
    def populate(self, param):
        self.populationMaxSize = param
        # generate first generation
        self.population = self.generate_population()
        
        # do some things
        while not self.stopping_condition():
            # selection, crossover, mutation
            current_population = self.selection(self.population)
            young_population = self.crossover(current_population)
            self.population = self.mutation(young_population)
            self.iterations += 1
        
        # get best member
        best_path = self.find_best()
        best_cost = self.cost(best_path.dna)
        
        # show results
        self.path = best_path.dna
        self.show_solution(best_cost)
        self.prd(best_cost)
    
    def stopping_condition(self):
        return self.iterations < self.MAX_ITERATIONS
    
    def selection(self, population: list[Member]) -> list[Member]:
        # normalize costs
        m = self.find_worst()
        Member.max_cost = m.cost
        for p in population:
            p.normalize()
        
        # selection
        new_population = []
        for i in range(0, math.floor(self.populationMaxSize * self.SELECTION_RATE)):
            # roulette
            c = random.random()
            index = 0
            
            while c > 0:
                c -= population[index].normalized_cost
                index += 1
            new_population.append(population[index - 1])
        return new_population
    
    def crossover(self, population: list[Member]) -> list[Member]:
        """
        https://user.ceng.metu.edu.tr/~ucoluk/research/publications/tspnew.pdf
        """
        new_population = []
        while len(new_population) < self.populationMaxSize:
            # get 2 parents randomly
            [p1, p2] = random.choices(population, k=2)
            dna1, dna2 = p1.dna, p2.dna
            # PMX
            crossover_point = random.randint(0, len(dna1))
            new_dna = dna1
            # mamy wyznaczony punkt przecięcia
            # przepisz na i-tym miejscu dna1 wartość z itego miejsca dna2
            # znajdz to co było na i-tym miejscu dna2 w dna1 i podstaw tam to co dotychczas było na i-tym miejscu w dna1
            for i in range(0, crossover_point):
                p = new_dna[i]
                q = dna2[i]
                new_dna[i] = dna2[i]
                new_dna[new_dna.index[q]] = p
            new_population.append(Member(new_dna))
        return new_population
    
    def mutation(self, population: list[Member]) -> list[Member]:
        for s in population:
            if self.MUTATION_RATE < random.random():
                e1, e2 = random.choices(s.dna, k=2)
                i1, i2 = s.dna.index(e1), s.dna.index(e2)
                s.dna[i1], s.dna[i2] = s.dna[i2], s.dna[i1]
        return population
        
    def find_best(self) -> Member:
        best = self.population[0]
        best_cost = self.cost(best.dna)
        for p in self.population:
            p_cost = self.cost(p.dna)
            if best_cost > p_cost:
                best_cost = p_cost
                best = p
        return best
    
    def find_worst(self) -> Member:
        worst = self.population[0]
        worst_cost = self.cost(worst.dna)
        for p in self.population:
            p_cost = self.cost(p.dna)
            if worst_cost < p_cost:
                worst_cost = p_cost
                worst = p
        return worst
    
    def generate_population(self) -> list[Member]:
        """
        generate starting population
        :return: population
        """
        population = []
        for i in range(1, self.populationMaxSize):
            new_member = [x for x in range(self.dimension)]
            random.shuffle(new_member)
            population.append(Member(new_member))
        return population
    
    def run(self, algorithm, param):
        if algorithm == 'genetic':
            self.populate(int(param))
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
