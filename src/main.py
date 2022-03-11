import sys

from src.read_tsp_instance import read_tsp_instance

if len(sys.argv) < 2:
  exit(1)

i = read_tsp_instance(sys.argv[1])
i.read()

# print(f"matrix {len(i.matrix)}")
# print(f"graph {len(i.graph)}")

print(f"Failed {sys.argv[1]}" if len(i.matrix) == 0 and len(i.graph) == 0 and 'GEO' in i.header else "Passed")
