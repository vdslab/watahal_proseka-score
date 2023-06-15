import json
from pprint import pprint

import constant
from classes.Notes import Note
from classes.types import HoldType, JudgeType, NotesType

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

notes_explain_to_index = {
    ne: i for i, ne in zip(range(len(notes_explain)), notes_explain)
}

judge_types = {
    i: x for x, i in zip(constant.JUDGE_TYPES, range(len(constant.JUDGE_TYPES)))
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

    notes_dict_for_json: list[dict] = []

    _score = None
    with open("score/data/m155.json", "r") as f:
        _score = json.load(f)

    for _note in _score["notes"]:
        note_dict = dict()
        notes: list[Note] = []
        for n, key in zip(_note, notes_explain):
            if key == "is_yellow":
                note_dict[key] = n != 1
            elif key == "judge_type":
                note_dict[key] = judge_types[n]
            elif key == "hold_type":
                note_dict[key] = hold_types[n]
            elif key == "type":
                note_dict[key] = types[n]
            else:
                note_dict[key] = n
        if note_dict["is_yellow"]:
            note_dict["type"] = "yellow"
        if "flick" in note_dict["judge_type"]:
            note_dict["type"] = "flick"

        note = Note(
            x=note_dict["x"],
            y=note_dict["y"],
            width=note_dict["width"],
            type=NotesType[note_dict["type"].upper()],
            judge_type=JudgeType[note_dict["judge_type"].upper()],
        )
        if note.is_hold:
            note.hold_type = HoldType[note_dict["hold_type"].upper()]
            note.hole = note_dict["hole"]
        assert note_dict == note.to_dict(), "not to dict error"
        assert note.to_dict() != note.__dict__, "own dict and __dict__ is same"

        print(_note)
        print(note_dict)
        print(notes_explain_to_index)
        x = _note[notes_explain_to_index["x"]]
        y = _note[notes_explain_to_index["y"]]
        width = _note[notes_explain_to_index["width"]]
        is_yellow = _note[notes_explain_to_index["is_yellow"]] != 1
        _type_id = _note[notes_explain_to_index["type"]]
        type_id = _type_id + 1 if is_yellow else _type_id
        judge_type_id = _note[notes_explain_to_index["judge_type"]]
        nn = Note(
            x=x,
            y=y,
            width=width,
            type=NotesType(type_id),
            judge_type=JudgeType(judge_type_id),
        )
        if nn.is_hold:
            hold_type_id = _note[notes_explain_to_index["hold_type"]]
            hole = _note[notes_explain_to_index["hole"]]
            note.hold_type = HoldType[hold_type_id]
            note.hold_type = hole

        print(nn)
        print(note)
        assert nn == note, "equal old note"
        assert nn != None, "none check"

        break
        notes_dict_for_json.append(note_dict)
        notes.append(note)

    # pprint(notes[:10])

    # score = dict()
    # with open(save_path, "w") as f:
    #     json.dump(notes, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
