import glob
import json
import re

from more_itertools import windowed


def get_bpm_info(file_path: str) -> list[dict] | None:
    song_info = None
    with open(file_path, "r") as f:
        song_info = json.load(f)

    if song_info is None:
        return None

    bpms_data = song_info["bpms"]
    notes_data = song_info["notes"]
    ys = [d[0] for d in notes_data]
    duration = int(max(ys) + 1)

    bpms: list[dict] = []
    for cur, next in windowed(bpms_data, 2):
        if next is None:
            bpms.append({"start": cur[0], "end": duration, "bpm": cur[1]})
            continue

        bpms.append({"start": cur[0], "end": next[0], "bpm": cur[1]})

    return bpms


def get_bpm_change2(original_data_path: str):
    bpms = get_bpm_info(original_data_path)
    if bpms is None:
        return None

    bpm_change_value = 0
    for prev, cur in windowed(bpms, 2):
        if prev is not None and cur is not None:
            bpm_change = cur["bpm"] - prev["bpm"]
            bpm_change_value += bpm_change * bpm_change
            continue

    return bpm_change_value


if __name__ == "__main__":
    original_data_paths = glob.glob("proseka/datas/*.json")
    original_data_paths = sorted(
        original_data_paths,
        key=lambda path: int(re.search(r"\d+", path).group()),
    )

    for path in original_data_paths[:100]:
        bpm_change_value = get_bpm_change2(path)

        print(f"{bpm_change_value=}")
