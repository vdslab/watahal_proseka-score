from pprint import pprint

from section_divide import get_section


def _get_feature_vector(section: list[dict]):
    # 曲特徴
    duration = 0
    note_density = 0
    note_types_count = dict()
    # x_shift：右にだんだんとずれていく=>値が大きい
    x_shift = 0
    consecutive_same_x_count_list = []
    # 運指特徴
    hand_balance = 0
    distances_between_notes_list = []


def get_feature_vectors(notes_json_file_relative_path: str):
    notes_sections = get_section(notes_json_file_relative_path)
    feature_vectors = []
    for section in notes_sections:
        vector = _get_feature_vector(section)
        feature_vectors.append(vector)

    return feature_vectors


if __name__ == "__main__":
    feature_vectors = get_feature_vectors("score/data/m155_notes.json")
    pprint(feature_vectors)
