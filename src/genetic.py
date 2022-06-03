
from __future__ import annotations


import numpy as np
from graph import Graph
import copy
import math
import random
from dotenv import load_dotenv
import csv
import os
import sys
import time
from collections import Counter

class Member:
    max_cost: int = 0
    population: Graph
    
    def __init__(self, dna):
        self.dna = np.copy(dna)
        self.cost = Member.population.cost(dna)
        self.age = 0
        self.normalized_cost = 0
        Member.max_cost = max(Member.max_cost, self.cost)
    
    def normalize(self, s):
        self.normalized_cost = self.cost / s


class Population(Graph):
    MAX_ITERATIONS: int = 100000
    SELECTION_RATE: float = 10
    MUTATION_RATE: float = 0.01
    POPULATION_MAX_SIZE: int = 128
    MAX_ITER_WITH_STAGNATION : int = 2000
    MAX_AGE : int = 10
    
    population: list[Member]
    iterations: int = 0
    
    def __init__(self):
        super().__init__()
        self.best = None
        Member.population = self
    
    def populate(self, param):
        start = time.time()
        params = [float(x) for x in param.split(",")]
        self.MAX_ITERATIONS = int(params[0])
        self.MUTATION_RATE = params[1]
        self.SELECTION_RATE = params[2]
        self.POPULATION_MAX_SIZE = int(params[3])
        self.MAX_ITER_WITH_STAGNATION = int(params[4])
        self.MAX_AGE = int(params[5])
        self.TYPE_OF = int(params[6])
        self.CROSSOVER_MODE = int(params[7])
        self.previous_best = 0
        self.population = self.generate_population()
        self.best = self.find_best(self.population)
        self.min_cost = self.best.cost
        self.path = self.best.dna
        self.prd(self.best.cost)

        stagnation=0
        
        while not self.stopping_condition():
            self.iter += 1
            #print(self.iter, ' POPULACJA')
            #for item in self.population:
            #    print("{} - {}".format(item.dna,item.cost))
            self.population = self.selection(self.population)
            self.population = self.crossover(self.population)
            self.population = self.mutation(self.population)
            self.population = self.add_age(self.population)
            best = self.find_best(self.population)
            if best.cost < self.min_cost:
                #print(best.dna)
                self.best = best
                self.min_cost = best.cost
                self.path = best.dna
                self.prd(best.cost)
                #print(self.path)
                #print(Counter(self.path))

            if self.previous_best==best.cost:
                stagnation += 1
            else:
                stagnation = 0
            self.previous_best=best.cost
            if stagnation>self.MAX_ITER_WITH_STAGNATION:
                if self.TYPE_OF:
                    self.population=self.unstack(self.population)
                else:
                    self.population.clear()
                    self.population=self.improve_atsp()
                    self.population = self.atsp_unstack(self.population)
                stagnation = 0

        
        #self.path = self.best.dna
        self.show_solution(self.min_cost)
        self.prd(self.min_cost)
        print(Counter(self.path))
        print(len(self.path))
        print(time.time()-start)
    
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

    def add_age(self,population):
        #print(population)
        for i in range(len(population)):
            population[i].age += 1
            #print(population[i].age, end =" ")
            if population[i].age > self.MAX_AGE:
                prev = population[i].cost
                if self.TYPE_OF:
                    population[i] = Member(self.two_opt_genetic(population[i].dna))
                else:
                    population[i] =self.unstack([population[i]])[0]
                if prev == population[i].cost:
                    population[i] = self.unstack([population[i]])[0]
            
        #print()
        return population
    
    def generate_population(self) -> list[Member]:
        population = []
        dna = [x for x in range(self.dimension)]
        for i in range(0, math.floor(self.POPULATION_MAX_SIZE/2)):
            new_dna_k = self.k_random_genetic(dna,10)
            new_dna = dna[:]
            random.shuffle(new_dna)
            population.append(Member(new_dna_k))
            population.append(Member(new_dna))
        return population
    
    def improve_atsp(self):
        population = []
        dna = [x for x in range(self.dimension)]
        for i in range(0, math.floor(self.POPULATION_MAX_SIZE/2)-5):
            new_dna_k = self.k_random_genetic(dna,10)
            new_dna = dna[:]
            random.shuffle(new_dna)
            population.append(Member(new_dna_k))
            population.append(Member(new_dna))
        for i in range(5):
            arr = self.nearest_neighbor(random.randint(0,self.dimension-1))
            population.append(Member(arr))
        population = self.unstack(population)
        population = self.unstack(population)
        return population


    def unstack(self,population) -> list[Member]:
        '''https://arxiv.org/ftp/arxiv/papers/1801/1801.07233.pdf (RGIBNNM)'''
        for i in range(len(population)):
            node_1 = random.randint(0,self.dimension-2)
            node_2 = random.randint(node_1+1,self.dimension-1)
            population[i].dna[node_1:node_2] = population[i].dna[node_1:node_2][::-1]
            random_gene = random.randint(0,self.dimension-1)
            closest_city = Member.population.one_nearest(random_gene)
            random_city = random.randint(closest_city-5,closest_city+5)
            if random_city < 0:
                random_city = 0
            if random_city > self.dimension-1:
                random_city = self.dimension-1
            population[i].dna[[closest_city,random_city]] = population[i].dna[[random_city,closest_city]]
            population[i].cost = Member.population.cost(population[i].dna)
            population[i].age = 0
        return population

    def atsp_unstack(self,population):
        for i in range(len(population)):
            tmp_list = population[i].dna.tolist()
            closest_city = Member.population.one_nearest(tmp_list[random.randint(0,math.floor(self.dimension/2))])
            closest_city_index = tmp_list.index(closest_city)
            tmp_list[0:closest_city_index] = reversed(tmp_list[0:closest_city_index])
            population[i] = Member(np.array(tmp_list))
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

        #Turniej
        #new_population = []
        #while(len(new_population) < self.POPULATION_MAX_SIZE):
        #    parents = random.choices(population, k=self.SELECTION_RATE)
        #    parents  = sorted(parents, key= lambda x:x.cost)
        #    new_population.append(parents[0])
        #    new_population.append(parents[1])
        #return new_population
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
        #Elitaryzm
        for i in range(5):
            new_population.append(population[i])
        for t1, t2 in zip(population[5::2], population[6::2]):
            if self.CROSSOVER_MODE:
                c1,c2 = self.cx(t1,t2)
            else:
                c1, c2 = self.pmx(t1, t2)
            new_population.append(Member(c1))
            new_population.append(Member(c2))
        '''for t1, t2 in zip(population[::2], population[1::2]):
            c1, c2 = self.pmx(t1, t2)
            new_population.append(Member(c1))
            new_population.append(Member(c2))'''
        return new_population
    
    # def prd(self, x):
    #     load_dotenv()
    #     ref = os.getenv(self.filename.split('\\')[-1].split('.')[0])
    #     if ref is None:
    #         print("reference value not found in .env")
    #         return
    #     ref = int(ref)
    #     # print(f"REF: {ref}; COST: {x}")
    #     result = 100 * (x - ref) / ref
    #     # print("PRD: {}%".format(result))
    #     # print(f"{self.iter}, {x}, {result}")
    #     with open('C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\tests\\out\\test3.csv', 'a') as fd:
    #         name = self.filename.split('\\')[-1]
    #         fd.write(f"{name}, {self.iter}, {self.MUTATION_RATE}, {self.SELECTION_RATE}, {self.POPULATION_MAX_SIZE}, "
    #                  f"{math.floor(x)}, {result}\n")
    
    def mutation(self, population: list[Member]) -> list[Member]:
        """
        Mutation is a genetic operator used to maintain genetic diversity from one generation of a population of
        genetic algorithm chromosomes to the next. It is analogous to biological mutation.
        """
        new_population = []
        for member in population:
            if random.random() < self.MUTATION_RATE:
                i1, i2 = np.random.choice(member.dna.shape[0], 2, replace=False)
                #i1 = 0
                if i1 > i2:
                    i1, i2 = i2, i1
                #i1,i2 = i2,i1
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

    def cx(self,t1,t2):
        cycle1 = []
        cycle2 = []
        parent1 = t1.dna.tolist()
        parent2 = t2.dna.tolist()
        first = parent1[0]
        first_index = parent1.index(first)
        cycle1.append(first)
        second = -1
        while second != cycle1[0]:
            second = parent2[first_index]
            first_index = parent1.index(second)
            first = parent1[first_index]
            cycle1.append(first)
        cycle1 = cycle1[:len(cycle1)-1]

        first = parent1[1]
        first_index = parent1.index(first)
        cycle2.append(first)
        second = -1
        while second != cycle2[0]:
            second = parent2[first_index]
            first_index = parent1.index(second)
            first = parent1[first_index]
            cycle2.append(first)
        cycle2 = cycle2[:len(cycle2)-1]

        child1 = parent1[:]
        child2 = parent2[:]

        for element in cycle2:
            index = parent2.index(element)
            child1[index] = element

        for element in cycle2:
            index = parent1.index(element)
            child2[index] = element

        #print("Child1: ",child1)
        #print("Child2: ",child2)

        return np.array(child1),np.array(child2)

    def hx(self,t1,t2):
         # t2 = Member(np.array([1, 2, 3, 4]))
        # t1 = Member(np.array([4, 1, 2, 3]))
        # self.dimension = 4
        pass


if __name__ == "__main__":
    Population.run()
