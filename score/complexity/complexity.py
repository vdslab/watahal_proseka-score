import glob
import json
from pprint import pprint

import numpy as np
from bpm import get_bpm_by_measure, get_bpm_change2
from density import get_y_densities_by_measure
from x_movement import get_x_diff_rates, get_x_movement_by_measure


def get_normal_notes(path: str):
    with open(path) as f:
        score = json.load(f)

    # flickが含まれる
    normal_notes = list(filter(lambda note: note["type"] == "normal", score))
    normal_notes = sorted(normal_notes, key=lambda note: (note["y"], note["x"]))
    return normal_notes


def calc_complexity():
    score_file_paths = glob.glob("score/data/notes_score/*.json")
    score_file_paths = sorted(
        score_file_paths, key=lambda path: int(path.split(".")[0].split("-")[1])
    )

    score_status = []

    # detail
    details = None
    with open("proseka/datas/detail/data.json") as f:
        details: list[dict] = json.load(f)

    for path in score_file_paths:
        # flickが含まれる
        normal_notes = get_normal_notes(path)
        x_diffs = get_x_diff_rates(normal_notes)

        # めっちゃぶれてた方がわかりやすいので平均値は大きい方がいい
        # そのぶれ方は，全体的に散ってた方がいいので標準偏差は小さい方がいい？ので逆数
        # かけ算だとそれっぽいので1以下にならないように1を足す
        # x_diff_status = np.mean(x_diffs) * (1 / np.std(x_diffs))
        x_diff_status = np.mean(x_diffs) * np.std(x_diffs)

        id = int(path.split(".")[0].split("-")[1])
        bpms = get_bpm_by_measure(id)
        bpm_ave = sum(bpms) / len(bpms)

        # 値が大きいほど変化が急なので単純でない．そのため逆数をとる
        bpm_change = get_bpm_change2(f"proseka/datas/song{id}.json")
        # bpm_change_status = 1 / (np.log(1 + bpm_change) + 1)
        bpm_change_status = np.log(1 + bpm_change) + 1

        y_densities = get_y_densities_by_measure(path, separate_measure=1) * bpm_ave
        # 密度は低ければ低いほど単純
        # そのばらつきも低いほど単純
        # ただしBPMが高いと単純でなくなる
        # y_densities_status = 1 / (np.mean(y_densities) * np.std(y_densities))
        y_densities_status = np.mean(y_densities) * np.std(y_densities)

        status = x_diff_status * bpm_change_status * y_densities_status * (1 / bpm_ave)

        cur_detail = list(filter(lambda detail: detail["id"] == id, details))[0]

        info = dict()
        info["id"] = id
        info["name"] = cur_detail["name"]
        info["level"] = cur_detail["level"]
        info["status"] = status
        # info["x_diff_stats"] = x_diff_stats
        # info["bpm_change_status"] = bpm_change_status
        # info["weighted_bpm"] = weighted_bpm
        # info["y_densities_stats"] = y_densities_stats
        score_status.append(info)

    # pprint(score_status)

    score_status = sorted(score_status, key=lambda info: info["status"], reverse=True)
    pprint(score_status)

    # details = sorted(details, key=lambda detail: detail["level"])
    # cnt_by_level = dict()
    # for detail in details:
    #     level = detail["level"]
    #     if level not in cnt_by_level:
    #         cnt_by_level[level] = 0
    #     cnt_by_level[level] += 1

    # in_cnt_by_level = dict()
    # for i, data in enumerate(score_status):
    #     level = data["level"]
    #     # if i < cnt_by_level[level]


if __name__ == "__main__":
    file_path = "score/data/notes_score/score-155.json"
    score = None
    with open(file_path) as f:
        score = json.load(f)
    score = sorted(score, key=lambda note: (note["y"], note["x"]))
    bm = get_bpm_by_measure(155)
    print(len(bm))
    print(bm)
