import json
from pprint import pprint

import constant

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
    i: x for x, i in zip(constant.JUDGLE_TYPES, range(len(constant.JUDGLE_TYPES)))
}

hold_types = {0: "none", 1: "start", 2: "end", 3: "middle"}

# NOTES_TYPES = [
#     "normal",
#     "yellow",
#     "hold",
#     "flick",
# ]
types = {1: "normal", 3: "long"}
types = {
    i + 1: x for x, i in zip(constant.NOTES_TYPES, range(len(constant.NOTES_TYPES)))
}


def main():
    save_dir = "score/data"
    save_file_name = "m155_notes-test.json"
    save_path = (
        save_dir + save_file_name
        if save_dir[-1] == "/"
        else f"{save_dir}/{save_file_name}"
    )

    notes: list[dict] = []

    _score = None
    with open("score/data/m155.json", "r") as f:
        _score = json.load(f)

    for _note in _score["notes"]:
        note = dict()
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
        # TODO enumでなんとかできてほしい
        # if note["is_yellow"]:
        #     note["type"] = "yellow"
        # TODO これもenumでなんとかできてほしい
        if "flick" in note["judge_type"]:
            note["type"] = "flick"
        notes.append(note)

    # pprint(notes[:10])

    # score = dict()
    with open(save_path, "w") as f:
        json.dump(notes, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
