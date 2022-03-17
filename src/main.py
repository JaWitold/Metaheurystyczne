import sys

from graph import Graph
from generate import GenerateGraph

if(sys.argv[1]=="generate"):
    if len(sys.argv)==6:
        i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]),int(sys.argv[5]))
    elif len(sys.argv)==5:
        i=GenerateGraph(sys.argv[2],int(sys.argv[3]),int(sys.argv[4]))
elif(sys.argv[1]=="load"):
    i = Graph(sys.argv[2])
else:
    print("Unsupported type")
    print("main.py <load> <filename>")
    print("OR")
    print("main.py <generate> <type> <dimension> <seed> <upper_bound (optional, default=100)>")
