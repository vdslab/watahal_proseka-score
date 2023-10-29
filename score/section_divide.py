import json

from arrange_score import get_notes_score
from classes import Note
from classes.types import HoldType


def _get_section(file_path: str) -> list[list[Note]]:
    score: list[Note] = get_notes_score(file_path)
    section_groups: list[list[Note]] = []
    section: list[Note] = []

    score_by_y: dict[float, list[Note]] = dict()
    for note in score:
        score_by_y.setdefault(note.y, []).append(note)

    score_by_y_ordered: list[tuple[float, list[Note]]] = sorted(
        score_by_y.items(), key=lambda x: x[0]
    )
    for y, notes in score_by_y_ordered:
        if len(notes) == 1:
            section.append(notes[0])
            continue

        section += notes

        have_middle = False
        for note in notes:
            if note.hold_type == HoldType.MIDDLE:
                have_middle = True
                break

        if have_middle:
            continue

        section_groups.append(section)
        section = notes

    if not section == score_by_y_ordered[-1][1]:
        section_groups.append(section)
        section.clear()

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
    print(len(notes_section_155), len(notes_section_155[0]))
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
