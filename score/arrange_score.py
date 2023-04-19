import json
from pprint import pprint

notes_explain = [
    "y",
    "type",
    "hole",
    "hold_type",
    "is_yellow",
    "judge_type",
    "x",
    "width",
]
judge_types = {
    0: "off",
    1: "flick",
    3: "flick_left",
    4: "flick_right",
    5: "push",
    6: "hold",
}
hold_types = {0: "none", 1: "start", 2: "end", 3: "middle"}
types = {1: "normal", 3: "long"}


def main():
    notes: list[dict] = []

    _score = None
    with open("score/data/m155.json", "r") as f:
        _score = json.load(f)

    for _note in _score["notes"]:
        note = dict()
        # print(_note)
        # print(notes_explain)
        for n, key in zip(_note, notes_explain):
            if key == "is_yellow":
                note[key] = n != 1
            elif key == "judge_type":
                note[key] = judge_types[n]
            elif key == "hold_type":
                note[key] = hold_types[n]
            elif key == "type":
                note[key] = types[n]
            else:
                note[key] = n
        # print(note)
        notes.append(note)

    # pprint(notes[:10])

    # score = dict()
    with open("score/data/m155_notes.json", "w") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
