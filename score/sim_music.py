import csv
import glob
import json
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


# @logger
# def euclidean_sim():
#     for pos in data_by_id[base_id]["positions"]:
#         for id in ids:
#             if id == base_id:
#                 continue
#             dists = []
#             sim_by_id[base_id][id] = 0

#             for target_pos in data_by_id[id]["positions"]:
#                 dists.append(math.dist(pos, target_pos))
#             dists = sorted(dists)
#             sim_by_id[base_id][id] += sum(dists[:20])


@logger
def save_similarity(
    save_file_path: str, source_id: str, similarity_by_id: dict[int, float]
):
    with open(save_file_path, "w") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "target", "similarity"])
        for target_id, similarity in similarity_by_id.items():
            writer.writerow([source_id, target_id, similarity])


@logger
def save_cos_similarity_all_combinations(
    vec_2dim_by_id: dict[int, list[list[float]]], save_dir_path: str
):
    """全ての組み合わせの類似度を計算して保存する
    # 引数
    - vec_2dim_by_id: { id_1: [[value_1, value_1, ..., value_n], ...], ... }
    - save_dir_path: 保存先ディレクトリパス
    ## vec_2dim_by_idの例:
    - { 1: [ [1, 2, 3], [4, 5, 6] ], 2: [ [7, 8, 9], [10, 11, 12] ] }
    ## 注意:
    - 各要素数は同じである必要がある
    - 保存される名前は `similarities_{id}.csv` となる
    """

    for source_id, source_vec_2dim in vec_2dim_by_id.items():
        similarity_by_id = dict()
        for target_id, target_vec_2dim in vec_2dim_by_id.items():
            if source_id == target_id:
                continue
            similarity_by_id[target_id] = cos_similarity(
                source_vec_2dim, target_vec_2dim
            )

        save_file_name = f"similarities_{source_id}.csv"
        save_file_path = os.path.join(save_dir_path, save_file_name)
        save_similarity(save_file_path, source_id, similarity_by_id)


@logger
def similarity_from_dim_reduce():
    save_dir_path = "./data/sims"
    os.makedirs(save_dir_path, exist_ok=True)

    clustering_data_path = "./data/_json/0930/clustering_result/clustering_data.csv"
    data = load_dict_csv(clustering_data_path)
    data = trim_data(data)

    ids = list({d["id"] for d in data})

    data_by_id = dict()
    for id in ids:
        id_data = [d for d in data if d["id"] == id]
        positions = [(d["x"], d["y"]) for d in id_data]
        data_by_id[id] = positions

    save_cos_similarity_all_combinations(data_by_id, save_dir_path)


@logger
def similarity_from_feature_vector():
    save_dir_path = "./data/sims"
    os.makedirs(save_dir_path, exist_ok=True)
    feature_vector_file_path = glob.glob(
        "./score/data/_json/feature_vector/test/*[[]test[]]*.json*"
    )

    data_by_id = dict()
    for path in feature_vector_file_path:
        with open(path) as f:
            feature_vector_data = json.load(f)
            data_by_id[feature_vector_data["id"]] = feature_vector_data["data"]

    save_cos_similarity_all_combinations(data_by_id, save_dir_path)


if __name__ == "__main__":
    similarity_from_dim_reduce()
    # similarity_from_feature_vector()
