import csv
import math
import pprint
import sys


def Print(string):
    sys.stdout.write("\033[2K\033[G")
    sys.stdout.write(string)
    sys.stdout.flush()


clustering_data_path = "./data/_json/0930/clustering_result/clustering_data.csv"
data = []
Print("loading data...")
with open(clustering_data_path) as f:
    reader = csv.DictReader(f)
    data = list(reader)
print("done")

Print("processing data...")
for i, d in enumerate(data):
    id = int(d["id"])
    category = None if d["category"] == "" else d["category"]
    x = float(d["x"])
    y = float(d["y"])
    label = int(d["label"])
    data[i] = {"id": id, "category": category, "label": label, "x": x, "y": y}
print("done")

Print("get ids...")
ids = list({d["id"] for d in data})
print("done")

Print("get positions...")
data_by_id = dict()
for id in ids:
    data_by_id[id] = dict()
    id_data = [d for d in data if d["id"] == id]
    positions = [(d["x"], d["y"]) for d in id_data]

    data_by_id[id]["positions"] = positions
print("done")


sim_by_id = dict()
for base_id in ids:
    Print("calculating similarity...")
    sim_by_id[base_id] = dict()
    for pos in data_by_id[base_id]["positions"]:
        for id in ids:
            if id == base_id:
                continue
            dists = []
            sim_by_id[base_id][id] = 0

            for target_pos in data_by_id[id]["positions"]:
                dists.append(math.dist(pos, target_pos))
            dists = sorted(dists)
            sim_by_id[base_id][id] += sum(dists[:20])
    print("done")

    Print(f"make {base_id} file...")
    save_file_path = f"./data/similarities_{base_id}.csv"
    with open(save_file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["base_id", "target_id", "similarity"])
        for base_id in sim_by_id:
            id_sims = sorted(sim_by_id[base_id].items(), key=lambda x: x[1])
            for target_id, sim in id_sims:
                writer.writerow([base_id, target_id, sim])
    print("done")
