import csv
import math
import os
import pprint
import sys

from sklearn.metrics.pairwise import cosine_similarity


def logger(func):
    def _wrapped(*args, **kwargs):
        sys.stdout.write("\033[2K\033[G")
        sys.stdout.write(f"do {func.__name__}...")
        sys.stdout.flush()

        v = func(*args, **kwargs)

        sys.stdout.write("\033[2K\033[G")
        sys.stdout.write(f"done {func.__name__}...")
        sys.stdout.flush()

        return v

    return _wrapped


save_dir_path = "./data/sims"
os.makedirs(save_dir_path, exist_ok=True)

clustering_data_path = "./data/_json/0930/clustering_result/clustering_data.csv"
data = []
logger("loading data...")
with open(clustering_data_path) as f:
    reader = csv.DictReader(f)
    data = list(reader)
print("done")

logger("processing data...")
for i, d in enumerate(data):
    id = int(d["id"])
    category = None if d["category"] == "" else d["category"]
    x = float(d["x"])
    y = float(d["y"])
    label = int(d["label"])
    data[i] = {"id": id, "category": category, "label": label, "x": x, "y": y}
print("done")

logger("get ids...")
ids = list({d["id"] for d in data})
print("done")

logger("get positions...")
data_by_id = dict()
for id in ids:
    data_by_id[id] = dict()
    id_data = [d for d in data if d["id"] == id]
    positions = [(d["x"], d["y"]) for d in id_data]

    data_by_id[id]["positions"] = positions
print("done")


sim_by_id = dict()
for base_id in ids:
    logger("calculating similarity...")
    sim_by_id[base_id] = dict()
    base_positions = data_by_id[base_id]["positions"]
    for id in ids:
        sim_metrics = cosine_similarity(base_positions, data_by_id[id]["positions"])
        ave_sims = []
        for sims in sim_metrics:
            order_sims = sorted(sims, reverse=True)
            slice_sims = order_sims[:20]
            ave_sims.append(sum(slice_sims) / len(slice_sims))
        sim_by_id[base_id][id] = sum(ave_sims) / len(ave_sims)
    # for pos in data_by_id[base_id]["positions"]:
    #     for id in ids:
    #         if id == base_id:
    #             continue
    #         dists = []
    #         sim_by_id[base_id][id] = 0

    #         for target_pos in data_by_id[id]["positions"]:
    #             dists.append(math.dist(pos, target_pos))
    #         dists = sorted(dists)
    #         sim_by_id[base_id][id] += sum(dists[:20])

    logger(f"make {base_id} file...")

    save_file_name = f"similarities_{base_id}.csv"
    save_file_path = os.path.join(save_dir_path, save_file_name)
    with open(save_file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["base_id", "target_id", "similarity"])
        for base_id in sim_by_id:
            id_sims = sorted(sim_by_id[base_id].items(), key=lambda x: x[1])
            for target_id, sim in id_sims:
                writer.writerow([base_id, target_id, sim])
    print("done")

    break
