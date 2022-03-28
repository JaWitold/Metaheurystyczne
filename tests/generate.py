import random


class GraphGenerator:
    supported_formats = ['FULL_MATRIX', 'EUC_2D', 'LOWER_DIAG_ROW']
    supported_format_keys = ['EDGE_WEIGHT_FORMAT', 'EDGE_WEIGHT_TYPE']
    supported_header_delimiters = ['NODE_COORD_SECTION', 'EDGE_WEIGHT_SECTION']
    edge_weight_format = ""
    matrix = []
    coordinates = dict()
    
    def __init__(self, variant, dimension, seed, upper_bound=100):
        self.variant = variant
        self.dimension = int(dimension)
        self.upper_bound = int(upper_bound)
        random.seed(int(seed))
    
    def generate(self):
        if self.variant == 'FULL_MATRIX':
            for i in range(self.dimension):
                row = []
                for j in range(self.dimension):
                    if i == j:
                        row.append(9999)
                    else:
                        row.append(random.randint(1, self.upper_bound))
                self.matrix.append(row)
        elif self.variant == 'EUC_2D':
            for ni in range(self.dimension):
                ni_x=random.randint(0,100)
                ni_y=random.randint(0,100)
                self.coordinates[int(ni+1)] = {'x': int(float(ni_x)), 'y': int(float(ni_y))}
            for i in range(self.dimension):
                row = []
                for j in range(self.dimension):
                    if i==j:
                        row.append(0) 
                        break
                    else:
                        row.append(int(round(((float(self.coordinates[i+1]['x']) - float(self.coordinates[j+1]['x'])) ** 2 + (float(self.coordinates[i+1]['y']) - float(self.coordinates[j+1]['y'])) ** 2) ** 0.5, 0)))
                self.matrix.append(row)
            for i in range(self.dimension):
                    for j in range(i + 1,self.dimension):
                        self.matrix[i].append(self.matrix[j][i])
        elif self.variant == 'LOWER_DIAG_ROW':
            for i in range(self.dimension):
                row = []
                for j in range(self.dimension):
                    if i == j:
                        row.append(0)
                        break
                    else:
                        row.append(random.randint(1, self.upper_bound))
                self.matrix.append(row)
            for i in range(self.dimension):
                for j in range(i + 1, self.dimension):
                    self.matrix[i].append(self.matrix[j][i])
        else:
            print("Unsupported type of problem, please choose one from list down below: ")
            for item in self.supported_formats:
                print(item)
            return
        # self.show_matrix()
        return self.matrix,self.coordinates
    
    def show_matrix(self):
        for row in self.matrix:
            print(row)
