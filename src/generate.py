import random
import sys
import copy
import time
class GenerateGraph:
	supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
	supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']
	supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']  
	edge_weight_format = ""
	matrix=[]
	

	def __init__(self,variant,dimension,seed,upper_bound=100):
		self.variant=variant
		self.dimension=dimension
		self.seed=random.seed(seed)
		self.upper_bound=upper_bound
		self.generate()
		self.show_solution()

	def generate(self):
		if(self.variant=='FULL_MATRIX'):
			for i in range(self.dimension):
				row=[]
				for j in range(self.dimension):
					if i==j:
						row.append(9999)
					else:
						row.append(random.randint(1,self.upper_bound))
				self.matrix.append(row)
		elif(self.variant=='EUC_2D'):
			for i in range(self.dimension):
				row=[]
				for j in range(self.dimension):
					if i==j:
						row.append(0)
						break
					else:
						value=random.randint((self.upper_bound/2)+1,self.upper_bound)
						row.append(value)
				self.matrix.append(row)
			for i in range(self.dimension):
				for j in range(i+1,self.dimension):
					self.matrix[i].append(self.matrix[j][i])

		elif(self.variant=='LOWER_DIAG_ROW'):
			for i in range(self.dimension):
				row=[]
				for j in range(self.dimension):
					if(i==j):
						row.append(0)
						break
					else:
						row.append(random.randint(1,self.upper_bound))
				self.matrix.append(row)
			for i in range(self.dimension):
				for j in range(i+1,self.dimension):
					self.matrix[i].append(self.matrix[j][i])
		else:
			print("Unsupported type of problem, please choose one from list down below: ")
			for item in self.supported_formats:
				print(item)
			return
		self.show_matrix()
		self.generate_path()

	def show_matrix(self):
		for row in self.matrix:
			print(row)

	def generate_path(self):
		print("Metoda k-random: ")
		self.k_random_method()
		print("Metoda najbliższego sąsiada: ")
		self.nearest_neighbor()
		print("Roszerzona metoda najbliższego sąsiada: ")
		self.extended_nearest_neighbor()
		print("Algorytm 2-OPT: ")
		self.two_opt()


	def k_random_method(self):
		k=100
		print("k: ",k)
		min_dist=sys.maxsize
		vertex=[x for x in range(self.dimension)]
		path=[]
		for j in range(k):
			random.shuffle(vertex)
			distance=0
			for i in range(len(vertex)):
				if i+1==len(vertex):
					distance=distance+self.matrix[vertex[i]][vertex[0]]
					break
				distance=distance+self.matrix[vertex[i]][vertex[i+1]]
			if(distance<min_dist):
				min_dist=distance
				path=vertex.copy()
		print("Droga: ",min_dist)
		print("Cykl: ",path)

	def nearest_neighbor(self):
		start=random.randint(0,self.dimension-1)
		print("Startowy wierzchołek: ",start)
		path=[start]
		min_dist=0
		matrix_copy=copy.deepcopy(self.matrix)
		while(len(path)!=self.dimension):
			distances=matrix_copy[start]
			distances.sort()
			counter=0
			j=0
			while j < self.dimension:
				if distances[counter]==self.matrix[start][j]:
					if j not in path:
						if(distances[counter]==0):
							counter=counter+1
							j=j-1
						else:
							min_dist=min_dist+distances[counter]
							path.append(j)
							start=j
							counter=0
							break
				j=j+1
				if(j==self.dimension):
					j=0 
					counter=counter+1
		print("Droga: ",min_dist)
		print("Cykl: ",path)



	def extended_nearest_neighbor(self):
		pass

	def cost(self,vertex):
		distance=0
		for i in range(len(vertex)):
			if i+1==len(vertex):
				distance=distance+self.matrix[vertex[i]][vertex[0]]
				break
			distance=distance+self.matrix[vertex[i]][vertex[i+1]]
		return distance

	def two_opt(self):
		path = [x for x in range(self.dimension)]
		best = path
		improved = True
		while improved:
			improved = False
			for i in range(0, len(path)-1):
				for j in range(i+1, len(path)):
					if j-i == 1: continue
					new_route = path[:]
					new_route[i:j] = reversed(new_route[i:j])
					if self.cost(new_route) < self.cost(best):
						best = new_route
						improved = True
			path = best
		print("Droga: ",self.cost(best))
		print("Cykl: ", path)


	def show_solution(self):
		pass
