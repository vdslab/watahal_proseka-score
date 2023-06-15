import json
from pprint import pprint

from classes.Notes import Note
from classes.types import HoldType, JudgeType, NotesType
from constant import NOTES_EXPLAIN

notes_explain_to_index = {
    ne: i for i, ne in zip(range(len(NOTES_EXPLAIN)), NOTES_EXPLAIN)
}


def main():
    save_dir = "score/data"
    save_file_name = "m155_notes-test.json"
    save_path = (
        save_dir + save_file_name
        if save_dir[-1] == "/"
        else f"{save_dir}/{save_file_name}"
    )

    _score = None
    with open("score/data/m155.json", "r") as f:
        _score = json.load(f)

    for _note in _score["notes"]:
        x = _note[notes_explain_to_index["x"]]
        y = _note[notes_explain_to_index["y"]]
        width = _note[notes_explain_to_index["width"]]
        # type
        is_yellow = _note[notes_explain_to_index["is_yellow"]] != 1
        _type_id = _note[notes_explain_to_index["type"]]
        type_id = _type_id + 1 if is_yellow else _type_id

        judge_type_id = _note[notes_explain_to_index["judge_type"]]

        note = Note(
            x=x,
            y=y,
            width=width,
            type=NotesType(type_id),
            judge_type=JudgeType(judge_type_id),
        )
        if note.is_hold:
            hold_type_id = _note[notes_explain_to_index["hold_type"]]
            hole = _note[notes_explain_to_index["hole"]]
            note.hold_type = HoldType[hold_type_id]
            note.hold_type = hole

        print(note)

        break
        notes.append(note)

    # pprint(notes[:10])

    # score = dict()
    # with open(save_path, "w") as f:
    #     json.dump(notes, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
