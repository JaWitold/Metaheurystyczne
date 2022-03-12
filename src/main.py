import sys

from readTSPInstance import ReadTSPInstance

if len(sys.argv) < 2:
    exit(1)

i = ReadTSPInstance(sys.argv[1])
i.read()

print(f"matrix {len(i.matrix)}")
print(f"graph {len(i.graph)}")
print(i.graph)

print(f"Failed {sys.argv[1]}" if len(i.matrix) == 0 and len(i.graph) == 0 and
                                 ('GEO' in i.header or 'UPPER_ROW' in i.header) else "Passed")
