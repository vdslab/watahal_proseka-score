import json
from pprint import pprint

import constant
import numpy
from classes import Note
from classes.types import NotesType
from move_score import _get_fingering
from section_divide import _get_section, get_section


def _get_section_feature_vector(section: list[Note]):
    # 区間特徴
    duration = section[-1].y - section[0].y

    note_types_count = {type.name: 0 for type in list(NotesType)}
    for note in section:
        note_types_count[note.type.name] += 1
    note_types_count_list = [note_types_count[key.name] for key in list(NotesType)]
    all_cnt = sum(note_types_count_list)

    move_sum = 0
    for i in range(len(section)):
        j = i
        while j < len(section) and section[j].y == section[i].y:
            j += 1
        if j >= len(section):
            continue
        move_sum += abs(section[i].x - section[j].x)

    # flip_count = 0
    # move_right = None
    # for i in range(len(section)):
    #     j = i
    #     while j < len(section) and section[j].y == section[i].y:
    #         j += 1
    #     if j >= len(section):
    #         continue

    #     if move_right is None:
    #         move_right = section[i].x < section[j].x
    #         continue
    #     if section[i].x < section[j].x and not move_right:
    #         flip_count += 1
    #     elif section[j].x < section[i].x and move_right:
    #         flip_count += 1
    #     move_right = section[i].x < section[j].x

    return [all_cnt, move_sum]


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


import math


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


import glob
import os
import re

if __name__ == "__main__":
    save_dir = "score/data/_json/feature_vector/test"
    os.makedirs(save_dir, exist_ok=True)
    # os.path.splitext(os.path.basename(filepath))[0]
    notes_file_paths = glob.glob("proseka/datas/*.json")
    notes_file_paths = [f for f in notes_file_paths if "155" in f]
    for file_path in notes_file_paths:
        fv = get_feature_vectors(file_path)
        save_file_name_base = os.path.splitext(os.path.basename(file_path))[0]
        id = re.split(r"(\D*)(\d*)", save_file_name_base)[2]
        try:
            id = int(id)
        except:
            raise RuntimeError("cannot convert id")

        save_file_name = f"{save_file_name_base}_[cnt_move]_fv.json"
        jsondata = {"id": id, "data": fv}
        with open(f"{save_dir}/{save_file_name}", "w", newline="") as sf:
            json.dump(jsondata, sf, indent=2, ensure_ascii=False)
