from pprint import pprint

import constant
import numpy
from move_score import get_fingering
from section_divide import get_section


def print_(str):
    print(f"[DEBUG]\t{str}")


def _get_section_feature_vector(section: list[dict]):
    # 区間特徴
    duration = section[-1]["y"] - section[0]["y"]

    # TODO
    note_density = 0

    note_types_count = {x: 0 for x in constant.NOTES_TYPES}
    for note in section:
        note_types_count[note["type"]] += 1
    note_types_count_list = [note_types_count[key] for key in constant.NOTES_TYPES]

    # x_shift：右にだんだんとずれていく=>値が大きい
    x_right_shift = 0
    consecutive_same_x_count_list = [0]
    for i in range(len(section) - 1):
        if section[i]["x"] == section[i + 1]["x"]:
            consecutive_same_x_count_list[-1] += 1
        else:
            if consecutive_same_x_count_list[-1] != 0:
                consecutive_same_x_count_list.append(0)

            if section[i]["x"] < section[i + 1]["x"]:
                x_right_shift += 1
            else:
                x_right_shift -= 1

    consecutive_same_x_average_variance = [
        numpy.average(consecutive_same_x_count_list),
        numpy.var(consecutive_same_x_count_list),
    ]

    if __debug__:
        print("section feature vector")
        print_(f"{duration=}")
        print_(f"{note_types_count=}")
        print_(f"{note_types_count_list=}")
        print_(f"{x_right_shift=}")
        print_(f"{consecutive_same_x_count_list=}")
        print_(f"{consecutive_same_x_average_variance=}")

    return (
        [duration]
        + note_types_count_list
        + [x_right_shift]
        + consecutive_same_x_average_variance
    )


def _get_fingering_feature_vector(fingering: dict):

    # 運指特徴
    hand_notes_count_balance = 0
    distances_between_notes_list = []
    left = fingering["left"]
    # right

    if __debug__:
        print_("fingering feature vector")
        print_(fingering)

    return []


def _get_feature_vector(section: list[dict], fingering: dict):
    section_feature_vector = _get_section_feature_vector(section)
    fingering_feature_vector = _get_fingering_feature_vector(fingering)

    if __debug__:
        print_("feature vector")
        print_(f"get section feature vector: {section_feature_vector}")
        print_(f"get fingering_feature_vector: {fingering_feature_vector}")
        print_(
            f"result: {section_feature_vector + fingering_feature_vector}",
        )

    return section_feature_vector + fingering_feature_vector


def get_feature_vectors(notes_json_file_relative_path: str):
    notes_sections = get_section(notes_json_file_relative_path)
    fingerings = get_fingering(notes_json_file_relative_path)
    # pprint(notes_sections[0])
    # pprint(fingerings)

    feature_vectors = []
    for (section, fingering) in zip(notes_sections, fingerings):
        vector = _get_feature_vector(section, fingering)
        feature_vectors.append(vector)

        if __debug__:
            break

    return feature_vectors


if __name__ == "__main__":
    feature_vectors = get_feature_vectors("score/data/m155_notes-test.json")
    pprint(feature_vectors)
