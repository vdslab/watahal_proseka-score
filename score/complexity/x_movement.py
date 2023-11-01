import json

import numpy as np
from more_itertools import windowed
from separate_score import separete_score_by_measure


def get_x_movement_by_measure(notes_by_measure: list[list[dict]]):
    x_movements = []
    for notes in notes_by_measure:
        x_moves = 0
        cnt = 0

        for cur, *res in windowed(notes, 5):
            if cur is None:
                break

            for note in res:
                if note is None:
                    continue

                x_moves += abs(cur["x"] - note["x"])
                cnt += 1
        x_movements.append(x_moves / cnt if cnt != 0 else 0)

    return x_movements


def get_x_diff_rates(notes: list[dict]):
    duration = int(max(notes, key=lambda note: note["y"])["y"] + 1)
    hist, bins = np.histogram(
        list(map(lambda note: note["y"], notes)),
        bins=duration,
        range=(0, duration),
    )
    rot = 0
    x_diffs = []

    for h in hist:
        range_notes = notes[rot : rot + h]
        before_same_y = False
        x_diff = 0
        cnt = 0

        for cur, next in windowed(range_notes, 2):
            if cur is None or next is None:
                continue

            if cur["y"] == next["y"]:
                before_same_y = True
                continue

            if before_same_y:
                before_same_y = False
                continue

            x_diff += abs(cur["x"] - next["x"])
            cnt += 1

        rot += h
        x_diffs.append(x_diff / cnt if cnt != 0 else 0)

    return x_diffs


if __name__ == "__main__":
    print(get_x_movement_by_measure([[{"x": 0}, {"x": 1}, {"x": 2}]]))
    score_id = 155
    file_path = f"score/data/notes_score/score-{score_id}.json"
    score = None
    with open(file_path) as f:
        score = json.load(f)

    if score is None:
        print("score not found")

    score_by_measure = separete_score_by_measure(score)
    print(get_x_movement_by_measure(score_by_measure))
