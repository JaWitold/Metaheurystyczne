import networkx as nx



class read_tsp_instance:
  matrix = []
  graph = nx.Graph()
  
  def __init__(self, filename):
    self.filename = filename
    self.header = dict()
  
  def read(self):
    with open(self.filename, 'r') as file:
      for line in file:
        if line.startswith('EDGE_WEIGHT_SECTION') or line.startswith('NODE_COORD_SECTION'):
          break
        else:
          line_split = line.replace(":", "").split()
          key = line_split[0]
          line_split.remove(key)
          value = ' '.join(str(e) for e in line_split)
          self.header.update({key: value})
      if('EDGE_WEIGHT_FORMAT' in self.header.keys()):
          key = 'EDGE_WEIGHT_FORMAT'
      elif ('NODE_COORD_SECTION' in self.header.keys()):
          key = 'EDGE_WEIGHT_FORMAT'
      elif ('EDGE_WEIGHT_TYPE' in self.header.keys()):
        key = 'EDGE_WEIGHT_TYPE'
      # print(self.header)
      
      if self.header[key] == 'FULL_MATRIX':
        self.read_full_matrix_to_matrix(file)
      elif self.header[key] == 'LOWER_DIAG_ROW':
        self.read_lower_diag_row_to_matrix(file)
      elif self.header[key] == 'EUC_2D':
        self.read_euc_2d(file)
      elif  self.header[key] == 'GEO':
        return
  
  def read_full_matrix_to_matrix(self, file):
    numbers = [item for sublist in [x.split() for x in file.readlines()] for item in sublist if item.isnumeric()]
    dimension = int(self.header["DIMENSION"])
    self.matrix = [[0 for y in range(0, dimension)] for x in range(0, dimension)]
    for i in range(0, dimension):
      for j in range(0, dimension):
        index = i * dimension + j
        self.matrix[i][j] = numbers[index]
  
  def read_lower_diag_row_to_matrix(self, file):
    # EDGE_WEIGHT_SECTION
    numbers = []
    for line in file:
      if line.startswith('DISPLAY_DATA_SECTION') or line.startswith('EOF'):
        break
      else:
        numbers.append(line.split())
    numbers = [int(item) for sublist in numbers for item in sublist]
    dimension = int(self.header["DIMENSION"])
    self.matrix = [[0 for y in range(0, x + 1)] for x in range(0, dimension)]
    
    index = 0
    for i in range(0, dimension):
      for j in range(0, i + 1):
        self.matrix[i][j] = numbers[index]
        index += 1
  
    # DISPLAY_DATA_SECTION
    self.read_euc_2d(file)
  
  def read_euc_2d(self, file):
    for line in file:
      if line.startswith('EOF'):
        break
      else:
        node = (line.split())
        if not node:
          break
        self.graph.add_node(int(node[0]), x=float(node[1]), y=float(node[2]))
        