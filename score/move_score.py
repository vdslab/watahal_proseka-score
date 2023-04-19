from collections import defaultdict
from pprint import pprint

import constant
from section_divide import get_section


def main():
    notes_section = get_section("score/data/m155_notes.json")
    for i, s in enumerate(notes_section):
        # section = notes_section[1]
        if i >= 3:
            break
        section = s
        print(section)
        notes_index_by_y = defaultdict(list[int])
        for i, note in enumerate(section):
            if note["hold_type"] == "middle":
                continue
            notes_index_by_y[note["y"]].append(i)
        # for i, note in enumerate(notes_index_by_y.items()):
        #     print(i, note)

        left = {"x": 0, "notes": [], "cost": 0}
        right = {"x": constant.MAX_KEYBOAD_COUNT, "notes": [], "cost": 0}

        def update_cost_from_index(
            section: list[list[dict]], hand: dict, note_index: int
        ) -> dict:
            hand["notes"].append(note_index)
            hand["cost"] += abs(hand["x"] - section[note_index]["x"])
            hand["x"] = section[note_index]["x"]
            return hand

        for note in notes_index_by_y.items():
            if len(note[1]) >= 2:
                left_note_index = note[1][0]
                left = update_cost_from_index(section, left, left_note_index)

                right_note_index = note[1][1]
                right = update_cost_from_index(section, right, right_note_index)
            else:
                note_index = note[1][0]
                left_move = abs(left["x"] - section[note_index]["x"])
                right_move = abs(right["x"] - section[note_index]["x"])
                if left_move <= right_move:
                    left = update_cost_from_index(section, left, note_index)
                else:
                    right = update_cost_from_index(section, right, note_index)
        print(left)
        print(right)
        print()


if __name__ == "__main__":
    main()
