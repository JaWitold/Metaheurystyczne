import csv

from ext_graph2 import ExtGraph

files = ["./out/cost_tsp.csv", "./out/cost_atsp.csv"]


times = dict()
for file in files:
    with open(file, "r") as csv_file:
        csv_reader = csv.DictReader(csv_file, fieldnames=['name', 'best_cost'])
        for row in csv_reader:
            print(row['name'])
            version = "ALL_tsp" if file == "./out/cost_tsp.csv" else "ALL_atsp"
            i = ExtGraph()
            command = f"C:\\Users\\user\\Desktop\\wppt\\metaheurystyczne\\vendors\\{version}\\{row['name']}\\{row['name']}"
            print(command)
            i.read(command)
            i.run_all("x", "x")

#
# with open("test3.csv", "w") as outfile:
#     writer = csv.writer(outfile)
#     key_list = list(times.keys())
#     writer.writerow(times.keys())
#     for i in range(len(times[key_list[0]])):
#         writer.writerow([times[x][i] for x in key_list])
