import glob
import json
import re

from bpm import get_bpm_by_measure


def get_display_bpm(original_path: str) -> int:
    id = int(re.search(r"\d+", original_path).group())
    data = None
    with open("proseka/datas/detail/data.json", "r") as f:
        data: list = json.load(f)

    detail = list(filter(lambda d: d["id"] == id, data))[0]
    return detail["bpm"]


def get_duration(path: str):
    data = None
    with open(path, "r") as f:
        data: list = json.load(f)

    if data is None:
        return None

    ys = [d[0] for d in data["notes"]]
    return int(max(ys) + 1)


def get_duration_weighted_average_bpm(original_path: str):
    bpms = get_bpm_by_measure(int(re.search(r"\d+", original_path).group()))
    # pprint(bpms)
    if bpms is None:
        print(f"Error. not found bpm info: {original_path}")
        return None

    return sum(bpms) / len(bpms)


if __name__ == "__main__":
    original_data_paths = glob.glob("proseka/datas/*.json")
    original_data_paths = sorted(
        original_data_paths,
        key=lambda path: int(re.search(r"\d+", path).group()),
    )

    for path in original_data_paths[154:155]:
        print(path)
        duration = get_duration(path)
        print(f"{duration=}")

        display_bpm = get_display_bpm(path)
        print(f"{display_bpm=}")

        weighted_bpm = get_duration_weighted_average_bpm(path)
        print(f"{weighted_bpm=}")
        print()
