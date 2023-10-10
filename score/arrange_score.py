import glob
import json
import os
import re

from classes.Notes import Note
from classes.types import HoldType, JudgeType, NotesType
from constant import NOTES_EXPLAIN

notes_explain_to_index = {
    ne: i for i, ne in zip(range(len(NOTES_EXPLAIN)), NOTES_EXPLAIN)
}


def get_notes_score(file_path: str) -> list[Note]:
    score = None
    with open(file_path, "r") as f:
        score = json.load(f)

    if score is None:
        return None

    notes: list[Note] = []

    for _note in score["notes"]:
        x = _note[notes_explain_to_index["x"]]
        y = _note[notes_explain_to_index["y"]]
        width = _note[notes_explain_to_index["width"]]
        # type
        is_yellow = _note[notes_explain_to_index["is_yellow"]] != 1
        type_id = _note[notes_explain_to_index["type"]]
        # type_id = _type_id + 1 if is_yellow else _type_id

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
            note.hold_type = HoldType(hold_type_id)
            note.hole = hole
            note.is_yellow = is_yellow

        notes.append(note)

        # if abs(note.y - 97.25) < 0.0001:
        #     print(note)

    return notes


def main():
    save_dir = "score/data/notes_score"
    os.makedirs(save_dir, exist_ok=True)

    file_paths = glob.glob("./proseka/datas/*.json")

    for path in file_paths:
        notes_score = get_notes_score(path)
        notes_score_dict = [note.to_dict() for note in notes_score]

        id_ = re.search(r"\d+", path).group()
        save_file_name = f"{id_}.json"

        save_path = os.path.join(save_dir, save_file_name)
        with open(save_path, "w") as f:
            json.dump(notes_score_dict, f, indent=2, ensure_ascii=False)
        # break


if __name__ == "__main__":
    main()
