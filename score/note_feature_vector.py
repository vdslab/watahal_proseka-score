import json
from pprint import pprint

import constant
import numpy
from classes import Note
from classes.types import NotesType
from move_score import _get_fingering
from section_divide import _get_section, get_section

# def print_(str):
#     print(f"[DEBUG]\t{str}")


def _get_section_feature_vector(section: list[Note]):
    # 区間特徴
    duration = section[-1].y - section[0].y

    note_types_count = {type.name: 0 for type in list(NotesType)}
    for note in section:
        note_types_count[note.type.name] += 1
    note_types_count_list = [note_types_count[key.name] for key in list(NotesType)]
    all_cnt = sum(note_types_count_list)
    # TODO
    note_density = duration / all_cnt

    # # x_shift：右にだんだんとずれていく=>値が大きい
    # x_right_shift = 0
    # consecutive_same_x_count_list = [0]
    # for i in range(len(section) - 1):
    #     if section[i]["x"] == section[i + 1]["x"]:
    #         consecutive_same_x_count_list[-1] += 1
    #     else:
    #         if consecutive_same_x_count_list[-1] != 0:
    #             consecutive_same_x_count_list.append(0)

    #         if section[i]["x"] < section[i + 1]["x"]:
    #             x_right_shift += 1
    #         else:
    #             x_right_shift -= 1

    # consecutive_same_x_average_variance = [
    #     numpy.average(consecutive_same_x_count_list),
    #     numpy.var(consecutive_same_x_count_list),
    # ]

    # if __debug__:
    #     print("section feature vector")
    #     print_(f"{duration=}")
    #     print_(f"{note_types_count=}")
    #     print_(f"{note_types_count_list=}")
    # print_(f"{x_right_shift=}")
    # print_(f"{consecutive_same_x_count_list=}")
    # print_(f"{consecutive_same_x_average_variance=}")

    return [note_density, all_cnt]
    return (
        [duration]
        + note_types_count_list
        # + [x_right_shift]
        # + consecutive_same_x_average_variance
    )


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

    # if __debug__:
    #     print_("fingering feature vector")
    #     print_(fingering)
    #     print_(f"{hand_notes_count_balance=}")
    #     print_(f"{distances_between_notes_list=}")
    #     print_(f"{distances_between_notes_average_variance=}")
    #     print_(
    #         f"fingering feature vector: {[hand_notes_count_balance] + distances_between_notes_average_variance}"
    #     )

    return [hand_notes_count_balance] + distances_between_notes_average_variance


def _get_feature_vector(section: list[Note], fingering: dict):
    section_feature_vector = _get_section_feature_vector(section)
    # fingering_feature_vector = _get_fingering_feature_vector(section, fingering)

    # if __debug__:
    #     print_("feature vector")
    #     print_(f"get section feature vector: {section_feature_vector}")
    # print_(f"get fingering_feature_vector: {fingering_feature_vector}")
    # print_(
    #     f"result: {section_feature_vector + fingering_feature_vector}",
    # )

    return section_feature_vector
    # return section_feature_vector + fingering_feature_vector


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


if __name__ == "__main__":
    feature_vectors = get_feature_vectors("score/data/m155.json")
    pprint(feature_vectors)

    save_dir = "score/data"
    save_file_name = "_dens_cnt_fv.json"
    save_path = (
        save_dir + save_file_name
        if save_dir[-1] == "/"
        else f"{save_dir}/{save_file_name}"
    )

    with open(save_path, "w") as f:
        json.dump(feature_vectors, f, indent=2, ensure_ascii=False)
