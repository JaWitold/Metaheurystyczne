from copy import deepcopy

from graph import Graph
import random


class Tabu(Graph):
    max_iterations = 1000
    max_stagnation_iterations = 10
    max_tabu_list_size = 7
    neighborhood_size = 10
    
    def __init__(self):
        self.iter = 0
        Graph.__init__(self)
    
    def tabu(self):
        s_best = [x for x in range(self.dimension)]
        best_path = deepcopy(s_best)
        random.shuffle(s_best)
        best_candidate = s_best
        no_opt_iterations = 0
        tabu_list = [s_best]
        print(s_best)

        while not self.stopping_condition():
            self.iter += 1
            s_neighborhood = self.get_neighbors(best_candidate)
            best_candidate = s_neighborhood[0]
            for sCandidate in s_neighborhood:
                if sCandidate not in tabu_list and self.fitness(sCandidate) > self.fitness(best_candidate):
                    best_candidate = sCandidate
            if self.fitness(best_candidate) > self.fitness(s_best):
                s_best = best_candidate
            else:
                no_opt_iterations += 1
            # stagnation
            if no_opt_iterations > self.max_stagnation_iterations:
                if self.fitness(s_best) > self.fitness(best_path):
                    cost = self.cost(best_path)
                    print(cost)
                    best_path = deepcopy(s_best)
                    tabu_list.clear()
                random.shuffle(s_best)
            tabu_list.append(best_candidate)
            if len(tabu_list) > self.max_tabu_list_size:
                tabu_list.pop(0)
        if self.fitness(s_best) > self.fitness(best_path):
            best_path = deepcopy(s_best)
        cost = self.cost(best_path)
        print(cost)
        return best_path
    
    def fitness(self, candidate):
        return 1 / self.cost(candidate)
    
    def stopping_condition(self):
        return self.iter > self.max_iterations
    
    # returns 10% of neighbourhood
    def get_neighbors(self, candidate):
        neighbors = []
        for i in range(0, len(candidate) // self.neighborhood_size):
            new_candidate = deepcopy(candidate)
            node_1 = random.randint(1, len(candidate) - 1)
            # node_2 = node_1 - 1
            node_2 = random.randint(0, len(candidate) - 1)
            # swap
            if node_1 == node_2:
                continue
            new_candidate[node_2], new_candidate[node_1] = new_candidate[node_1], new_candidate[node_2]
            neighbors.append(new_candidate)

        return neighbors


if __name__ == "__main__":
    tab = Tabu()
    tab.generate("EUC_2D", 50, 100)
    print(tab.tabu())
