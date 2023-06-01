from pprint import pprint

from move_score import get_fingering
from section_divide import get_section


def _get_section_feature_vector(section: list[dict]):
    print("section feature vector")
    # 区間特徴
    pprint(section)
    duration = section[0]
    note_density = 0
    note_types_count = dict()
    # x_shift：右にだんだんとずれていく=>値が大きい
    x_shift = 0
    consecutive_same_x_count_list = []
    return []


def _get_fingering_feature_vector(fingering: dict):
    print("fingering feature vector")
    print(fingering)
    # 運指特徴
    hand_notes_count_balance = 0
    distances_between_notes_list = []
    left = fingering["left"]
    # right
    return []


def _get_feature_vector(section: list[dict], fingering: dict):
    print("feature vector")
    section_feature_vector = _get_section_feature_vector(section)
    print("get section feature vector: ", section_feature_vector)
    fingering_feature_vector = _get_fingering_feature_vector(fingering)
    print("get fingering_feature_vector: ", fingering_feature_vector)
    print("result: ", section_feature_vector + fingering_feature_vector)
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

    return feature_vectors


if __name__ == "__main__":
    feature_vectors = get_feature_vectors("score/data/m155_notes.json")
    pprint(feature_vectors)
