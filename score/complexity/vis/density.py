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


def get_y_density(score_ys: list[int], *, separate_measure: int = 1) -> list[int]:
    hist, bins = np.histogram(
        score_ys,
        bins=(max(score_ys) + 1) // separate_measure,
        range=(0, max(score_ys) + 1),
    )
    print(f"{bins=}")
    return hist


if __name__ == "__main__":
    score_file_paths = glob.glob("score/data/notes_score/*.json")
    score_file_paths = sorted(
        score_file_paths, key=lambda path: int(path.split(".")[0].split("-")[1])
    )

    for path in score_file_paths[:1]:
        score_pos = get_score_pos(path)
        if score_pos is None:
            print(f"Error. not found score: {path}")
            continue

        ys = list(map(lambda note: note["y"], score_pos))
        pprint(get_y_density(ys))
