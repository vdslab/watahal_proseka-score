import json
import pprint


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
    notes_section = get_section("score/data/m155_notes.json")
    # pprint.pprint(notes_section)
    for section in notes_section:
        print(len(section))
    # if notes_section:
    #     pprint.pprint(notes_section[2])


if __name__ == "__main__":
    main()
