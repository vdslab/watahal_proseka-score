import csv
import glob
import json
import os
import sys

import matplotlib.pyplot as plt
import numpy as np
from sklearn import preprocessing
from sklearn.cluster import DBSCAN
from sklearn.manifold import TSNE
from sklearn.metrics import (  # silhouette_score,
    accuracy_score,
    f1_score,
    multilabel_confusion_matrix,
    precision_score,
    recall_score,
)
from sklearn.neighbors import NearestNeighbors


def get_kdist_plot(X=None, k=None, radius_nbrs=1.0):
    nbrs = NearestNeighbors(n_neighbors=k, radius=radius_nbrs).fit(X)

    # For each point, compute distances to its k-nearest neighbors
    distances, indices = nbrs.kneighbors(X)

    distances = np.sort(distances, axis=0)
    distances = distances[:, k - 1]

    # Plot the sorted K-nearest neighbor distance for each point in the dataset
    plt.figure(figsize=(8, 8))
    plt.plot(distances)
    plt.xlabel("Points/Objects in the dataset", fontsize=12)
    plt.ylabel("Sorted {}-nearest neighbor distance".format(k), fontsize=12)
    plt.grid(True, linestyle="--", color="black", alpha=0.4)
    plt.ylim((0, 0.2))
    plt.show()
    plt.close()


def readCSV(file_path, parse_func) -> list[list]:
    data = None
    with open(file_path, newline="") as csvfile:
        reader = csv.reader(csvfile)
        data: list[list] = []
        for row in reader:
            row_data = []
            for d in row:
                row_data.append(parse_func(d))
            data.append(row_data)

    return data


def acc_est(clustering_result, quiet=False):
    return _est(
        clustering_result,
        "./data/note_sims/sim_acc.csv",
        "./data/note_sims/not_sim_acc.csv",
        quiet,
    )


def est(clustering_result, quiet=False):
    return _est(
        clustering_result,
        "./data/note_sims/sim.csv",
        "./data/note_sims/not_sim.csv",
        quiet,
    )


def _est(clustering_result, sim_file_path, nsim_file_path, quiet=False):
    count = len(clustering_result)
    labels = {True: 1, False: 0, None: "none"}
    result_table = [
        [labels[i == j] for j in clustering_result] for i in clustering_result
    ]
    sim_table = [[labels[None] for _ in clustering_result] for _ in clustering_result]
    # _sim_table = [[None for _ in clustering_result] for _ in clustering_result]
    sim_data = readCSV(sim_file_path, int)
    not_sim_data = readCSV(nsim_file_path, int)
    if not sim_data or sim_data is None or len(sim_data) == 0:
        print("load error")
        return
    if not not_sim_data or not_sim_data is None or len(not_sim_data) == 0:
        print("load error")
        return

    for [s, t] in sim_data:
        sim_table[s][t] = labels[True]
        sim_table[t][s] = labels[True]
    for [s, t] in not_sim_data:
        sim_table[s][t] = labels[False]
        sim_table[t][s] = labels[False]

    sims_true = []
    sims = []
    for i in range(count):
        for j in range(i + 1, count):
            if sim_table[i][j] == labels[None]:
                continue

            sims_true.append(sim_table[i][j])
            sims.append(result_table[i][j])

    confusion_matrix = multilabel_confusion_matrix(sims_true, sims)
    accuracy = accuracy_score(sims_true, sims)
    precision = precision_score(sims_true, sims)
    recall = recall_score(sims_true, sims)
    f1 = f1_score(sims_true, sims)

    if not quiet:
        print("\n===== 評価 =====")
        print(np.array([["tp rate", "fn rate"], ["tn rate", "tn rate"]]))
        for label, matrix in zip(labels.values(), confusion_matrix):
            print(f"{label=}")
            sm = sum(sum(matrix))
            print(f"{matrix/sm}")
        print(f"{accuracy=}")
        print(f"{precision=}")
        print(f"{recall=}")
        print(f"{f1=}")
        print("=================\n")
    # print(f"accuracy = {accuracy_score()}")
    return accuracy, precision, recall, f1


# 保存先のファイル作成と列名記述
save_dir = "./data/_json/0729/clustering_result/umap"
save_file_name = "clustering_data.csv"
os.makedirs(save_dir, exist_ok=True)
with open(f"{save_dir}/{save_file_name}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "x", "y", "label", "category"])
print("make save file")


print(sys.path)
notes_file_paths = glob.glob(
    "./score/data/_json/feature_vector/test/*[[]test[]]*.json*"
)
# 学習元のデータ取得
train_notes_file_paths = [f for f in notes_file_paths if "155" in f]
train_notes_file_paths += [f for f in notes_file_paths if "318" in f]
train_data2d = []
for file_path in train_notes_file_paths:
    # data = None
    # id = None
    with open(file_path, newline="") as f:
        content = json.load(f)
        train_data2d.append(content["data"])

train_data = preprocessing.StandardScaler().fit_transform(
    np.array(sum(train_data2d, []))
)
print("get train data")

# カテゴリ名の取得
category_by_id = dict()
ids_318 = set()
sim_data_label = None
with open("./score/data/note_sims/sim_label_318.csv", newline="") as f:
    reader = csv.reader(f)
    content = [row for row in reader]
    header = content[0]
    print(content[1:3])
    sim_data_label = [[int(row[0]), int(row[1]), row[2]] for row in content[1:]]
    for row in content[1:]:
        category_by_id[int(row[0])] = row[2]
        category_by_id[int(row[1])] = row[2]
        ids_318.add(int(row[0]))
        ids_318.add(int(row[1]))
# _data = []
# ids = []
# lengths = []
# id_by_path = dict()
# data_by_id = dict()
for file_path in notes_file_paths:
    print(file_path)
    # if "155" in file_path or "318" in file_path:
    #     continue
    # データ準備
    _data = None
    id = None
    with open(file_path, newline="") as f:
        content = json.load(f)

        id = content["id"]
        _data = content["data"]

    if _data is None or id is None:
        raise RuntimeError

    _data = preprocessing.StandardScaler().fit_transform(np.array(_data))
    data = np.concatenate([train_data, _data])

    clustering_result = DBSCAN(eps=0.14, min_samples=3).fit_predict(data)
    clustering_result += 1

    categories_by_label: dict[int, list[str]] = dict()
    result_318 = clustering_result[
        len(train_data2d[0]) : len(train_data2d[0]) + len(train_data2d[1])
    ]
    # ラベルごとにカテゴリ名の配列を作成
    for i in ids_318:
        label = result_318[i]
        category = category_by_id[i]
        categories_by_label[label] = categories_by_label.get(label, []) + [category]
    # 文字列として加工しなおす
    for key in categories_by_label:
        cs = categories_by_label.get(key, [""])
        categories_by_label[key] = ",".join(set(("，".join(set(cs))).split("，")))
    categories_by_label[0] = "その他"
    categories_by_label: dict[int, str]

    # umap = UMAP(n_components=2, random_state=0)
    # dim_less_data = umap.fit_transform(data)
    # 次元削減
    tsne = TSNE(n_components=2, random_state=0)
    dim_less_data = tsne.fit_transform(data)

    sep_data = dim_less_data[len(train_data) :]
    sep_result = clustering_result[len(train_data) :]
    if len(sep_data) != len(_data):
        print(f"{len(sep_data)=}")
        print(f"{len(_data)=}")
        raise RuntimeError

    # 列名に合うように加工
    clustering_data = [
        [
            id,
            float(pos[0]),
            float(pos[1]),
            int(l),
            categories_by_label.get(int(l), None),
        ]
        for (pos, l) in zip(sep_data, sep_result)
    ]

    with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerows(clustering_data)

    print("make data")


# _data = []
# ids = []
# lengths = []
# id_by_path = dict()
# data_by_id = dict()
# for file_path in notes_file_paths:
#     # data = None
#     # id = None
#     with open(file_path, newline="") as f:
#         content = json.load(f)

#         # id = content["id"]
#         if "155" in f or "318" in f:
#             train_data += content["data"]
#         _data += content["data"]
#         ids.append(content["id"])
#         lengths.append(len(content["data"]))
#         id_by_path[file_path] = content["id"]

#     # k = 2 * len(data[0]) - 1 # k=2*{dim(dataset)} - 1
#     # get_kdist_plot(X=data, k=k)
# if len(_data) == 0:
#     raise RuntimeError
# _data = preprocessing.StandardScaler().fit_transform(np.array(_data))


# def clustering(data, eps):
#     clustering_result = DBSCAN(eps=eps, min_samples=3).fit_predict(data)
#     clustering_result += 1
#     return clustering_result


# def dim_reduce_tsne(data):
#     tsne = TSNE(n_components=2, random_state=0)
#     data_tsne = tsne.fit_transform(data)
#     return data_tsne


# def clustering_tsne_plot(data, eps):
#     data_tsne = dim_reduce_tsne(data)
#     clustering_result = clustering(data, eps)

#     plt.scatter(data_tsne[:, 0], data_tsne[:, 1], c=clustering_result, cmap="gist_ncar")
#     plt.show()


# clustering_result = clustering(train_data)
# clustering_tsne_plot(data, 0.1)
# clustering_result = DBSCAN(eps=0.14, min_samples=3, n_jobs=-1).fit_predict(data)
# clustering_result += 1


# import datetime
# import os


# def save_clustering_tsne_data(data, eps, save_dir, save_file_name):
#     os.makedirs(save_dir, exist_ok=True)
#     with open(f"{save_dir}/{save_file_name}", "w", newline="") as f:
#         writer = csv.writer(f)
#         writer.writerow(["id", "x", "y", "label"])
#     clustering_result = clustering(data, eps)
#     data_tsne = dim_reduce_tsne(data)
#     # 各区間ごとのデータ

#     data_idx = 0
#     for idx, length in zip(ids, lengths):
#         sep_data = data_tsne[data_idx : data_idx + length]
#         sep_result = clustering_result[data_idx : data_idx + length]
#         data_idx += length
#         clustering_data = [
#             [idx, float(pos[0]), float(pos[1]), int(l)]
#             for (pos, l) in zip(sep_data, sep_result)
#         ]

#         with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
#             writer = csv.writer(f)
#             writer.writerows(clustering_data)


# save_dir = "./data/_json/0727/clustering_result"
# save_file_name = "clustering_data.csv"
# save_clustering_tsne_data(_data, 0.14, save_dir, save_file_name)
