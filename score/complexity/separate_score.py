import json
from pprint import pprint

import numpy as np
from bpm import get_bpm_info


def get_notes_count_by_measure(score) -> list[int]:
    ys = list(map(lambda note: note["y"], score))
    duration = int(max(ys) + 1)
    hist, _ = np.histogram(
        ys,
        bins=duration,
        range=(0, duration),
    )

    return hist


def separete_score_by_measure(score):
    score = sorted(score, key=lambda note: (note["y"], note["x"]))

    notes_count_by_measure = get_notes_count_by_measure(score)

    current_count = 0
    score_by_measure = []

    for notes_count in notes_count_by_measure:
        sub_score = score[current_count : current_count + notes_count]
        score_by_measure.append(sub_score)
        current_count += notes_count

    return score_by_measure


if __name__ == "__main__":
    score_id = 155
    file_path = f"score/data/notes_score/score-{score_id}.json"
    score = None
    with open(file_path) as f:
        score = json.load(f)

    if score is None:
        print("score not found")

    score_by_measure = separete_score_by_measure(score)
    print(get_bpm_info(f"proseka/datas/song{score_id}.json"))
