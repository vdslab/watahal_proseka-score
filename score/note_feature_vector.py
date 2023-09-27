import glob
import json
import os
import re

import numpy
from classes import Note
from classes.types import NotesType
from move_score import _get_fingering
from section_divide import _get_section


def _get_section_feature_vector(section: list[Note]):
    # 区間特徴
    # duration = section[-1].y - section[0].y

    # ノーツの個数
    note_types_count = {type.name: 0 for type in list(NotesType)}
    for note in section:
        note_types_count[note.type.name] += 1
    note_types_count_list = [note_types_count[key.name] for key in list(NotesType)]
    all_cnt = sum(note_types_count_list)

    # 移動量の合計
    move_sum = 0
    for i in range(len(section)):
        j = i
        while j < len(section) and section[j].y == section[i].y:
            j += 1
        if j >= len(section):
            continue
        move_sum += abs(section[i].x - section[j].x)

    # 最初と最後の同時押しを除いた，半開区間，[start, end)
    def get_y_half_open_interval():
        start_idx = 0
        j = start_idx
        while j < len(section) and section[j].y == section[start_idx].y:
            j += 1
        start_idx = j

        end_idx = len(section)
        j = end_idx
        while j > 0 and section[j - 1].y == section[end_idx - 1].y:
            j -= 1
        end_idx = j
        return start_idx, end_idx

    # 左右のブレの回数
    start, end = get_y_half_open_interval()
    flip_count = 0
    flip_costs = []
    move_right = None
    for i in range(start, end - 1):
        if move_right is None:
            move_right = section[i].x < section[i + 1].x
            flip_costs.append(abs(section[i].x - section[i + 1].x))
            continue
        if section[i].x < section[i + 1].x and not move_right:
            flip_count += 1
            flip_costs.append(abs(section[i].x - section[i + 1].x))
        elif section[i + 1].x < section[i].x and move_right:
            flip_count += 1
            flip_costs.append(abs(section[i].x - section[i + 1].x))
        move_right = section[i].x < section[i + 1].x

    flip_cost_ave = sum(flip_costs) / len(flip_costs) if len(flip_costs) != 0 else 0

    alternately_moving_distance = [0, 0]
    for i in range(start, end):
        if i - 2 >= start:
            alternately_moving_distance[i % 2] += abs(section[i].x - section[i - 2].x)
    alternately_moving_distance_ave = sum(alternately_moving_distance) / len(
        alternately_moving_distance
    )

    # 階段の段数
    step_nums = []
    move_right = None
    for i in range(start, end - 1):
        if move_right is None:
            move_right = section[i].x < section[i + 1].x
            step_nums.append(0)
            continue

        if move_right:
            if section[i].x < section[i + 1].x:
                step_nums[-1] += 1
            elif section[i].x > section[i + 1].x:
                move_right = False
                step_nums.append(0)
        else:
            if section[i].x > section[i + 1].x:
                step_nums[-1] += 1
            elif section[i].x < section[i + 1].x:
                move_right = True
                step_nums.append(0)

    step_nums = list(filter(lambda x: x != 0, step_nums))
    # step_num_ave = sum(step_nums) / (len(step_nums)) if len(step_nums) != 0 else 0

    # 連続した個数
    consecutive_counts = [0]
    for i in range(start, end - 1):
        if section[i].x == section[i + 1].x:
            consecutive_counts[-1] += 1
        else:
            consecutive_counts.append(0)

    consecutive_counts = list(filter(lambda x: x != 0, consecutive_counts))
    consecutive_count_ave = (
        sum(consecutive_counts) / (len(consecutive_counts))
        if len(consecutive_counts) != 0
        else 0
    )

    return [
        all_cnt,
        # move_sum,
        flip_count,
        flip_cost_ave,
        alternately_moving_distance_ave,
        consecutive_count_ave,
        # step_num_ave*1000,
    ]


def _get_fingering_feature_vector(section: list[dict], fingering: dict):
    # 運指特徴
    # left divided by right ; left/right
    hand_notes_count_balance = 0
    distances_between_notes_list = []

    left: list = fingering["left"]
    right: list = fingering["right"]

    left_note_count = 0
    right_note_count = 0
    # print_(left)
    # for l, r in zip(left, right):
    left_note_count += len(left["notes"])
    right_note_count += len(right["notes"])

    for li, lnote_index in enumerate(left["notes"]):
        for ri in range(max(0, li - 1), min(len(right["notes"]), li + 2)):
            distances_between_notes_list.append(
                abs(section[lnote_index]["x"] - section[right["notes"][ri]]["x"])
            )
    hand_notes_count_balance = left_note_count / right_note_count
    distances_between_notes_average_variance = [
        numpy.average(distances_between_notes_list),
        numpy.var(distances_between_notes_list),
    ]

    return [hand_notes_count_balance] + distances_between_notes_average_variance


def _get_feature_vector(section: list[Note], fingering: dict):
    section_feature_vector = _get_section_feature_vector(section)
    # fingering_feature_vector = _get_fingering_feature_vector(section, fingering)

    return section_feature_vector


def get_feature_vectors(notes_json_file_relative_path: str):
    notes_sections = _get_section(notes_json_file_relative_path)
    fingerings = _get_fingering(notes_json_file_relative_path)

    feature_vectors = []
    for section, fingering in zip(notes_sections, fingerings):
        vector = _get_feature_vector(section, fingering)
        feature_vectors.append(vector)

        # if __debug__:
        #     break

    for i, vector in enumerate(feature_vectors):
        feature_vectors[i] = list(map(lambda x: round(x, 3), vector))

    return feature_vectors


if __name__ == "__main__":
    save_dir = "score/data/_json/feature_vector/test"
    os.makedirs(save_dir, exist_ok=True)
    # os.path.splitext(os.path.basename(filepath))[0]
    notes_file_path_search = glob.glob("proseka/datas/*.json")
    notes_file_paths = [f for f in notes_file_path_search if "155" in f or "318" in f]
    notes_file_paths = notes_file_path_search
    print(notes_file_paths)
    for file_path in notes_file_paths:
        fv = get_feature_vectors(file_path)
        save_file_name_base = os.path.splitext(os.path.basename(file_path))[0]
        id = re.split(r"(\D*)(\d*)", save_file_name_base)[2]
        try:
            id = int(id)
        except:
            raise RuntimeError("cannot convert id")

        save_file_name = f"{save_file_name_base}_[test]_fv.json"
        jsondata = {"id": id, "data": fv}
        with open(f"{save_dir}/{save_file_name}", "w", newline="") as sf:
            json.dump(jsondata, sf, indent=2, ensure_ascii=False)
