import glob
import json
import re
from pprint import pprint

from more_itertools import windowed


def get_bpm_info(file_path: str) -> list[dict] | None:
    song_info = None
    with open(file_path, "r") as f:
        song_info = json.load(f)

    if song_info is None:
        return None

    bpms_data = song_info["bpms"]
    bpms: list[dict] = []
    for bpm in bpms_data:
        bpms.append({"start": bpm[0], "bpm": bpm[1]})

    return bpms


if __name__ == "__main__":
    original_data_paths = glob.glob("proseka/datas/*.json")
    original_data_paths = sorted(
        original_data_paths,
        key=lambda path: int(re.search(r"\d+", path).group()),
    )

    for path in original_data_paths[154:155]:
        bpms = get_bpm_info(path)
        if bpms is None:
            print(f"Error. not found bpm info: {path}")
            continue

        pprint(bpms)
        bpm_change_value = 0
        for prev, cur in windowed(bpms, 2):
            print(prev, cur)
            duration = cur["start"] - prev["start"]
            bpm_change = cur["bpm"] - prev["bpm"]
            bpm_change_value += bpm_change * bpm_change
            print(f"{duration=}", f"{bpm_change=}")
        print(f"{bpm_change_value=}")
