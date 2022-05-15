from copy import deepcopy

from graph import Graph
import math
import random

# osobnik populacji
class Subject:
    permutation = []
    cost = 0


class Population(Graph):
    max_iterations = 1000
    selection_rate = 0.7
    mutation_rate = 0.05
    
    population = []
    iterations = 0
    
    def __init__(self):
        super().__init__()
        self.populationMaxSize = 128
    
    def populate(self):
        while not self.stopping_condition():
            current_population = self.selection(self.population)
            young_population = self.crossover(current_population)
            young_population = self.mutation(young_population)
            self.population = self.combine_old_n_young(current_population + young_population)
            self.iterations += 1
    
    def stopping_condition(self):
        return self.iterations < self.max_iterations
    
    def selection(self, population: list) -> list:
        for s in population:
            s.cost = self.cost(s.population)
        sorted_population = sorted(self.population, key=lambda x: x.cost, reverse=True)
        
        return sorted_population[0:math.floor(self.selection_rate * self.populationMaxSize)]
    
    def crossover(self, current_population: list) -> list:
        # TODO
        return []
    
    @staticmethod
    def mutation(young_population: list) -> list:
        for s in young_population:
            if random.randint(0, 1) == 1:
                p, q = random.choices(s.permutation, k=2)
                a, b = s.index(p), s.index(q)
                s[a], s[b] = s[b], s[a]
        return young_population
    
    def combine_old_n_young(self, current_population) -> list:
        for s in current_population:
            s.cost = self.cost(s.population)
        sorted_population = sorted(self.population, key=lambda x: x.cost, reverse=True)
        return sorted_population[0:128]
