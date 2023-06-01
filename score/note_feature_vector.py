from pprint import pprint

from section_divide import get_section


def _get_feature_vector(section: list[dict]):
    pass


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
