from section_divide import get_section
from pprint import pprint


def main():
    notes_section = get_section("score/data/m155_notes.json")
    pprint(notes_section[0])


if __name__ == "__main__":
    main()
