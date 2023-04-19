from section_divide import get_section
from pprint import pprint
from collections import defaultdict
import constant


def main():
    notes_section = get_section("score/data/m155_notes.json")
    pprint(notes_section[0])
    section = notes_section[0]
    notes_index_by_y = defaultdict(list[int])
    for i, note in enumerate(section):
        notes_index_by_y[note["y"]].append(i)
    for note in notes_index_by_y.items():
        print(note)


if __name__ == "__main__":
    main()
