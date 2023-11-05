import glob
import json
from pprint import pprint

import numpy as np


def get_score_pos(file_path: str) -> list[dict] | None:
    score = None
    with open(file_path, "r") as f:
        score = json.load(f)

    if score is None:
        return None

    score_pos = list(
        map(
            lambda note: {"x": note["x"], "y": note["y"], "width": note["width"]}, score
        )
    )
    return score_pos


def calc_y_densities_by_measure(
    score_ys: list[int], *, separate_measure: int = 1
) -> list[int]:
    hist, bins = np.histogram(
        score_ys,
        bins=int(max(score_ys) + 1) // separate_measure,
        range=(0, max(score_ys) + 1),
    )
    density = np.array(hist, dtype="float64") / separate_measure

    return density


def get_y_densities_by_measure(notes_data_path: str, *, separate_measure: int = 1):
    score_pos = get_score_pos(notes_data_path)
    if score_pos is None:
        return None

    ys = list(map(lambda note: note["y"], score_pos))
    return calc_y_densities_by_measure(ys, separate_measure=separate_measure)


if __name__ == "__main__":
    score_file_paths = glob.glob("score/data/notes_score/*.json")
    score_file_paths = sorted(
        score_file_paths, key=lambda path: int(path.split(".")[0].split("-")[1])
    )

    for path in score_file_paths[:1]:
        pprint(get_y_densities_by_measure(path))
