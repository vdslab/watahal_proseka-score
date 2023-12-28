import glob
import json
import os
import re
from pprint import pp, pprint

from move_score import get_fingering
from term_printer import Color, cprint


def main():
    file_paths = glob.glob("./proseka/datas/*.json")
    file_paths = sorted(
        file_paths, key=lambda path: int(re.search(r"\d+", path).group())
    )
    save_dir = "./score/data/_json/1228/fingering"
    os.makedirs(save_dir, exist_ok=True)
    for path in file_paths:
        cprint(f"{path=}", attrs=[Color.GREEN])

        data_notes_count = 0
        id = int(re.search(r"\d+", path).group())
        with open(f"score/data/notes_score/score-{id}.json", "r") as f:
            notes = json.load(f)
            data_notes_count = len(notes)
        # print(data_notes_count)

        fingering = get_fingering(path)
        # print(fingering)
        # print(len(fingering["left"]), len(fingering["right"]))
        fingering_notes_count = len(fingering["left"]) + len(fingering["right"])

        # assert (
        #     fingering_notes_count == data_notes_count
        # ), f"{fingering_notes_count=}, {data_notes_count=}"

        name = os.path.splitext(os.path.basename(path))[0]
        with open(f"{save_dir}/{name}.json", "w", newline="") as f:
            json.dump(fingering, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
