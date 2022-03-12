import sys

from src.graph import Graph

if len(sys.argv) < 2:
    exit(1)

i = Graph(sys.argv[1])
