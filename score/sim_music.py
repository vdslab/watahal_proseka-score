import csv
import math
import os
import sys

from sklearn.metrics.pairwise import cosine_similarity


def logger(func):
    def _wrapped(*args, **kwargs):
        sys.stdout.write(f"do {func.__name__}...")
        sys.stdout.flush()

        v = func(*args, **kwargs)

        sys.stdout.write("\033[2K\033[G")
        sys.stdout.flush()
        print(f"done {func.__name__}")

        return v

    return _wrapped


@logger
def load_dict_csv(file_path: str) -> list[dict] | None:
    data = None
    with open(file_path) as f:
        reader = csv.DictReader(f)
        data = list(reader)
    return data


@logger
def trim_data(data: list[dict]) -> list[dict]:
    for i, d in enumerate(data):
        id = int(d["id"])
        category = None if d["category"] == "" else d["category"]
        x = float(d["x"])
        y = float(d["y"])
        label = int(d["label"])
        data[i] = {"id": id, "category": category, "label": label, "x": x, "y": y}
    return data


def top_average_cos_sim(sims, top_n) -> float:
    order_sims = sorted(sims, reverse=True)
    slice_sims = order_sims[:top_n]
    return sum(slice_sims) / len(slice_sims)


def top_average_cos_sim_metrics(sim_metrics, top_n) -> float:
    ave_sims = []
    for sims in sim_metrics:
        ave_sims.append(top_average_cos_sim(sims, top_n))
    return sum(ave_sims) / len(ave_sims)


def cos_similarity(vec1, vec2) -> float:
    sim_metrics = cosine_similarity(vec1, vec2)
    ave_sim_metrics = top_average_cos_sim_metrics(sim_metrics, 20)
    return ave_sim_metrics


@logger
def save_similarity(
    save_file_path: str, source_id: str, similarity_by_id: dict[int, float]
):
    with open(save_file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "similarity"])
        for target_id, similarity in similarity_by_id.items():
            writer.writerow([source_id, target_id, similarity])


save_dir_path = "./data/sims"
os.makedirs(save_dir_path, exist_ok=True)

clustering_data_path = "./data/_json/0930/clustering_result/clustering_data.csv"
data = load_dict_csv(clustering_data_path)
data = trim_data(data)

ids = list({d["id"] for d in data})

data_by_id = dict()
for id in ids:
    data_by_id[id] = dict()
    id_data = [d for d in data if d["id"] == id]
    positions = [(d["x"], d["y"]) for d in id_data]
    data_by_id[id]["positions"] = positions


sim_by_id = dict()
for base_id in ids:
    print("calculating similarity...")
    sim_by_id[base_id] = dict()
    base_positions = data_by_id[base_id]["positions"]

    @logger
    def calc_sim():
        for id in ids:
            if id == base_id:
                continue

            sim_by_id[base_id][id] = cos_similarity(
                base_positions, data_by_id[id]["positions"]
            )

    @logger
    def euclidean_sim():
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

    calc_sim()
    # euclidean_sim()

    save_file_name = f"similarities_{base_id}.csv"
    save_file_path = os.path.join(save_dir_path, save_file_name)
    save_similarity(
        save_file_path, source_id=base_id, similarity_by_id=sim_by_id[base_id]
    )
    print(f"made id:{base_id} file\n")
