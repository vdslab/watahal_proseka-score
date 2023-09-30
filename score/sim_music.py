import csv
import math
import pprint

clustering_data_path = "./data/_json/0727/clustering_result/clustering_data.csv"
data = []
with open(clustering_data_path) as f:
    reader = csv.DictReader(f)
    data = list(reader)


for i, d in enumerate(data):
    id = int(d["id"])
    category = None if d["category"] == "" else d["category"]
    x = float(d["x"])
    y = float(d["y"])
    label = int(d["label"])
    data[i] = {"id": id, "category": category, "label": label, "x": x, "y": y}


ids = list({d["id"] for d in data})

data_by_id = dict()
for id in ids:
    data_by_id[id] = dict()
    id_data = [d for d in data if d["id"] == id]
    positions = [(d["x"], d["y"]) for d in id_data]

    data_by_id[id]["positions"] = positions

sim_by_id = dict()
for base_id in ids:
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

with open("./data/similarities.csv", "w") as f:
    writer = csv.writer(f)
    writer.writerow(["base_id", "target_id", "similarity"])
    for base_id in sim_by_id:
        id_sims = sorted(sim_by_id[base_id].items(), key=lambda x: x[1])
        for target_id, sim in id_sims:
            writer.writerow([base_id, target_id, sim])
