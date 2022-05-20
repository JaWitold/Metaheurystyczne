import sys
from graph import Graph
from genetic import Population
mode = sys.argv[1]
i = Population()

if mode == "generate":
    algorithm = sys.argv[2]
    i.generate(sys.argv[4], sys.argv[5], sys.argv[6])
    i.run(algorithm, sys.argv[3])
elif mode == "load":
    algorithm = sys.argv[3]
    i.read(sys.argv[2])
    i.run(algorithm, sys.argv[4])
else:
    print("UNSUPPORTED TYPE \n"
          "USAGE: \n"
          "main.py load <filename> <algorithm> <params> OR \n"
          "main.py generate <algorithm> <params> <type> <dimension> <seed> <upper_bound (optional, default=100)>\n"
          "WHERE algorithm IS ONE OF \"k-random\", \"nearest-neighbor\" , \"extended-nearest-neighbor (in this option <params> must be 'none' \" OR \"two-opt\"")
          
