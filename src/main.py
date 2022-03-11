import sys

from src.open import read_tsp_instance

if len(sys.argv) < 2:
  exit(1)

i = read_tsp_instance(sys.argv[1])
i.read()

print(i.matrix)
print(i.graph)