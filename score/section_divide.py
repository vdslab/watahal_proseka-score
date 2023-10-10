import json

from arrange_score import get_notes_score
from classes import Note
from classes.types import HoldType


def _get_section(file_path: str) -> list[list[Note]]:
    score: list[Note] = get_notes_score(file_path)
    section_groups: list[list[Note]] = []
    section: list[Note] = []
    i = 0
    while i < len(score):
        j = i
        same_y_start_id = j
        same_y = False
        same_y_middle_count = 0
        while j + 1 < len(score):
            if same_y and score[j].hold_type == HoldType.MIDDLE:
                same_y_middle_count += 1

            if same_y and score[j].y != score[j + 1].y:
                count = j - same_y_start_id + 1
                if same_y_middle_count / count <= 0.5:
                    break

                same_y = False
                same_y_start_id = j

            if score[j].y == score[j + 1].y:
                same_y = True
                same_y_start_id = j

            j += 1

        for k in range(i, min(j + 1, len(score))):
            section.append(score[k])
        section_groups.append(section)
        section.clear()
        for k in range(same_y_start_id, min(j + 1, len(score))):
            section.append(score[k])

        i = j + 1
    return section_groups


def divider(notes: list[dict]) -> list[list[dict]]:
    """
    同時押しが2つだけの場合のみ対応
    """

    notes_sim_press_section: list[list[dict]] = []
    group: list[dict] = []
    notes_len = len(notes)
    for i in range(notes_len):
        group.append(notes[i])

        if i + 1 >= notes_len:
            continue

        same_y = notes[i]["y"] == notes[i + 1]["y"]
        is_middle = (
            notes[i]["hold_type"] == "middle" or notes[i + 1]["hold_type"] == "middle"
        )
        if not same_y or is_middle:
            continue

        # 現在区間の終了
        group.append(notes[i + 1])

        # 次の区間を探す準備
        notes_sim_press_section.append(group)
        group = [notes[i]]
        # print("new group")
        # pprint.pprint(group)
    return notes_sim_press_section


def get_section(file_path: str) -> list[list[dict]] | None:
    """
    ノーツJSONを，同時押しの区間で分けれられたものを作成
    """
    notes = None
    with open(file_path) as f:
        _notes = json.load(f)
        notes = sorted(_notes, key=lambda note: (note["y"], note["x"]))

    if notes:
        notes_sim_press_section = divider(notes)
        return notes_sim_press_section

    return None


def main():
    # notes_section_318 = _get_section("proseka/datas/song318.json")
    # for section in notes_section_318:
    #     fin = False
    #     for n in section:
    #         print(n)
    #         if n.y >= 14:
    #             fin = True
    #     print("===============================")
    #     if fin:
    #         return

    notes_section_155 = _get_section("score/data/m155.json")
    for section in notes_section_155:
        fin = False
        if section[0].y < 100 or 115 < section[0].y:
            continue
        if not (section[0].is_hold and section[1].is_hold):
            continue
        for n in section:
            print(n)
        print("===============================")
        if fin:
            return


if __name__ == "__main__":
    main()
