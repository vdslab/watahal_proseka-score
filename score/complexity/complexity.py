import glob
import json
import os
from pprint import pprint

import numpy as np
from bpm import get_bpm_by_measure, get_bpm_change2
from density import get_y_densities_by_measure
from separate_score import separate_score_by_measure
from x_movement import get_x_diff_rates, get_x_movement_by_measure


def get_normal_notes(path: str):
    with open(path) as f:
        score = json.load(f)

    # flickが含まれる
    normal_notes = list(filter(lambda note: note["type"] == "normal", score))
    normal_notes = sorted(normal_notes, key=lambda note: (note["y"], note["x"]))
    return normal_notes


def get_x_locations(score_by_measure):
    x_locations = []
    for measure in score_by_measure:
        xs = [note["x"] for note in measure]
        x_locations.append(np.std(xs) if len(xs) > 0 else 0)
    return x_locations


def get_push_at_once_count_averages(score_by_measure):
    push_at_once_count_averages = []
    for measure in score_by_measure:
        ys = [note["y"] for note in measure]
        ys_count = dict()
        for y in ys:
            if y not in ys_count:
                ys_count[y] = 0
            ys_count[y] += 1
        # print(measure)
        counts = ys_count.values()
        push_at_once_count_averages.append(
            sum(counts) / len(counts) if len(counts) > 0 else 0
        )
    return push_at_once_count_averages


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
        id = int(path.split(".")[0].split("-")[1])
        bpms = get_bpm_by_measure(id)

        score = None
        with open(path) as f:
            score = json.load(f)
        score_by_measure = separate_score_by_measure(score)
        x_locates = get_x_locations(score_by_measure)
        push_at_once_count_averages = get_push_at_once_count_averages(score_by_measure)
        x_moves = get_x_movement_by_measure(score_by_measure)
        y_densities = get_y_densities_by_measure(path, separate_measure=1)

        status_by_measure = []
        for i in range(len(score_by_measure)):
            if score_by_measure[i] == []:
                continue
            status_by_measure.append(
                x_moves[i]
                + (bpms[i] / 3) * y_densities[i]
                + bpms[i]
                + 1 / (x_locates[i] + 1)
                + push_at_once_count_averages[i]
            )
        status = np.mean(status_by_measure)

        cur_detail = list(filter(lambda detail: detail["id"] == id, details))[0]

        info = dict()
        # info["id"] = id
        info["name"] = cur_detail["name"]
        info["level"] = cur_detail["level"]
        info["status"] = status
        # info["bpm"] = np.mean(bpms)
        score_status.append(info)

    score_status = sorted(score_status, key=lambda info: info["status"], reverse=True)
    pprint(score_status)
    os.makedirs("score/data/complexity", exist_ok=True)
    with open("score/data/complexity/complexity.json", "w") as f:
        score = json.dump(score_status, f, ensure_ascii=False, indent=2)
    # pprint(score_status[-5:])

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
    calc_complexity()
