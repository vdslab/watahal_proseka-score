import glob
import json
import re

from more_itertools import windowed


def get_bpm_by_measure(score_id: int) -> list[dict]:
    bpm_info = get_bpm_info(score_id)
    bpm_info_index = 0
    duration = bpm_info[-1]["end"]
    bpm_by_measure = []
    for measure in range(duration - 1):
        bpm_sum = 0
        bpm_count = 0
        while True:
            if bpm_info_index >= len(bpm_info):
                break
            cur_bpm_info = bpm_info[bpm_info_index]

            current_bpm_in_measure_range = (
                measure <= cur_bpm_info["start"] < measure + 1
            )

            next_bpm_in_measure_range = measure < cur_bpm_info["end"] <= measure + 1
            bpm_in_measure_range = (
                current_bpm_in_measure_range and next_bpm_in_measure_range
            )
            if bpm_in_measure_range:
                bpm_sum += cur_bpm_info["bpm"]
                bpm_count += 1
                bpm_info_index += 1
                continue

            if current_bpm_in_measure_range and not next_bpm_in_measure_range:
                bpm_sum += cur_bpm_info["bpm"]
                bpm_count += 1
                bpm_info_index += 1
                break

            bpm_sum += cur_bpm_info["bpm"]
            bpm_count += 1
            break

        if bpm_count > 0:
            bpm_by_measure.append(bpm_sum // bpm_count)

        if bpm_info_index >= len(bpm_info):
            bpm_by_measure.append(bpm_info[-1]["bpm"])

    return bpm_by_measure


def get_bpm_info(id: int) -> list[dict] | None:
    song_info = None
    with open(f"proseka/datas/song{id}.json", "r") as f:
        song_info = json.load(f)

    if song_info is None:
        return None

    bpms_data = song_info["bpms"]
    notes_data = song_info["notes"]
    ys = [d[0] for d in notes_data]
    duration = int(max(ys) + 1)

    if len(bpms_data) == 1:
        return [{"start": 0, "end": duration, "bpm": bpms_data[0][1]}]

    bpms: list[dict] = []
    for cur, next in windowed(bpms_data, 2):
        bpms.append({"start": cur[0], "end": next[0], "bpm": cur[1]})
    bpms.append({"start": bpms_data[-1][0], "end": duration, "bpm": bpms_data[-1][1]})

    return bpms


def get_bpm_change2(original_data_path: str):
    id = int(re.search(r"\d+", original_data_path).group())
    bpms = get_bpm_by_measure(id)
    if bpms is None:
        return None

    bpm_change_value = 0
    for prev, cur in windowed(bpms, 2):
        if prev is not None and cur is not None:
            bpm_change = abs(cur - prev)
            bpm_change_value += bpm_change * bpm_change
            continue

    return bpm_change_value


if __name__ == "__main__":
    original_data_paths = glob.glob("proseka/datas/*.json")
    original_data_paths = sorted(
        original_data_paths,
        key=lambda path: int(re.search(r"\d+", path).group()),
    )

    for path in original_data_paths:
        bpm_change_value = get_bpm_change2(path)

        print(path, f"{bpm_change_value=}")
