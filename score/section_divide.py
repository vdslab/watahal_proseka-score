import json

from arrange_score import get_notes_score
from classes import Note
from classes.types import HoldType


def _get_section(file_path: str) -> list[list[Note]]:
    score: list[Note] = get_notes_score(file_path)
    section_groups: list[list[Note]] = []
    section: list[Note] = []
    print("score count length", len(score))

    score_by_y: dict[float, list[Note]] = dict()
    for note in score:
        score_by_y.setdefault(note.y, []).append(note)

    ly = 0
    ex = 0

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

        ly += len(section)
        section_groups.append(section)
        section = notes

        ex += len(notes)

    if not section == score_by_y_ordered[-1][1]:
        ly += len(section)
        section_groups.append(section)
        # section.clear()

    # print(f"{ly}, {ex}, {ly-ex=}")
    # print("sum", sum(map(len, section_groups)))

    # section_groups = list(filter(lambda x: len(x) >= 1, section_groups))
    return section_groups


def main():
    notes_section_155 = _get_section("proseka/datas/song324.json")
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
