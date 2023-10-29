"""
譜面が複雑であるとはを考えるより，単純であることを考えるほうがやさしいという感覚

譜面が単純であるとは
main
- 交互押せばいいことが明確に分かる（どうやってとればいいかがわかりやすい）
    - 左右のブレが大きい
    - 「左右のブレが少ないところ」が多い（「」が少ないと片手連打で取ればいいかってなりそう）

sub : 譜面が「簡単」である尺度な気がする
- BPMの変化が少ない（bpm.pyのget_bpm_change2）
    - 簡単か単純かにしろ，違和感がある
- ノーツの密度が低い / 密度の変化が少ない（density.pyのget_y_density）
"""

"""
譜面が難しいということ

「難しい」とき，「複雑」であるかという命題
- 譜面が「難しくない」とき，「単純」は直感にあう
- 譜面が「複雑」なとき，「難しい」も直感的
対偶：「複雑でない」とき，「難しくない」⇔「単純」なとき，「難しくない」

ちょっとした反例
その譜面は「単純」だけど「難しい」というとき
- 楽曲が早ければ早いほど，クリアができないという意味で「難しい」
- そもそも押せないという状況になる

「難しい」にかかる言葉
- クリアができない（から難しい）
- ミスが発生しやすい
- どうノーツを取ればいいかが分からない
- 指が追い付かない

つまり，譜面が難しいとは，「ノーツの速度が速い」と「譜面が複雑」のどちらかが成り立つとき
それぞれは独立
難しさの度合いを上の2つで表せそう
"""

import glob
import json
from pprint import pprint

import numpy as np
from more_itertools import windowed
from speed import get_duration_weighted_average_bpm
from vis.bpm import get_bpm_change2
from vis.density import get_y_densities


def get_normal_notes(path: str):
    with open(path) as f:
        score = json.load(f)

    # flickが含まれる
    normal_notes = list(filter(lambda note: note["type"] == "normal", score))
    normal_notes = sorted(normal_notes, key=lambda note: (note["y"], note["x"]))
    return normal_notes


def get_x_diff_rates(notes: list[dict]):
    duration = int(max(normal_notes, key=lambda note: note["y"])["y"] + 1)
    hist, bins = np.histogram(
        list(map(lambda note: note["y"], normal_notes)),
        bins=duration,
        range=(0, duration),
    )
    rot = 0
    x_diffs = []

    for h in hist:
        range_notes = normal_notes[rot : rot + h]
        before_same_y = False
        x_diff = 0
        cnt = 0

        for cur, next in windowed(range_notes, 2):
            if cur is None or next is None:
                continue

            if cur["y"] == next["y"]:
                before_same_y = True
                continue

            if before_same_y:
                before_same_y = False
                continue

            x_diff += abs(cur["x"] - next["x"])
            cnt += 1

        rot += h
        x_diffs.append(x_diff / cnt if cnt != 0 else 0)

    return x_diffs


if __name__ == "__main__":
    score_file_paths = glob.glob("score/data/notes_score/*.json")
    score_file_paths = sorted(
        score_file_paths, key=lambda path: int(path.split(".")[0].split("-")[1])
    )

    score_info = []
    score_status = []

    # detail
    details = None
    with open("proseka/datas/detail/data.json") as f:
        details: list[dict] = json.load(f)

    for path in score_file_paths:
        # flickが含まれる
        normal_notes = get_normal_notes(path)
        x_diffs = get_x_diff_rates(normal_notes)

        # めっちゃぶれてた方がわかりやすいので平均値は大きい方がいい
        # そのぶれ方は，全体的に散ってた方がいいので標準偏差は小さい方がいい？ので逆数
        # かけ算だとそれっぽいので1以下にならないように1を足す
        # x_diff_status = np.mean(x_diffs) * (1 / np.std(x_diffs))
        x_diff_status = np.mean(x_diffs) * np.std(x_diffs)

        id = int(path.split(".")[0].split("-")[1])
        weighted_bpm = get_duration_weighted_average_bpm(f"proseka/datas/song{id}.json")

        # 値が大きいほど変化が急なので単純でない．そのため逆数をとる
        bpm_change = get_bpm_change2(f"proseka/datas/song{id}.json")
        # bpm_change_status = 1 / (np.log(1 + bpm_change) + 1)
        bpm_change_status = np.log(1 + bpm_change) + 1

        y_densities = get_y_densities(path, separate_measure=1) * weighted_bpm
        # 密度は低ければ低いほど単純
        # そのばらつきも低いほど単純
        # ただしBPMが高いと単純でなくなる
        # y_densities_status = 1 / (np.mean(y_densities) * np.std(y_densities))
        y_densities_status = np.mean(y_densities) * np.std(y_densities)

        status = (
            x_diff_status * bpm_change_status * y_densities_status * (1 / weighted_bpm)
        )

        cur_detail = list(filter(lambda detail: detail["id"] == id, details))[0]

        info = dict()
        info["id"] = id
        info["name"] = cur_detail["name"]
        info["level"] = cur_detail["level"]
        info["status"] = status
        # info["x_diff_stats"] = x_diff_stats
        # info["bpm_change_status"] = bpm_change_status
        # info["weighted_bpm"] = weighted_bpm
        # info["y_densities_stats"] = y_densities_stats
        score_status.append(info)

    # pprint(score_status)

    score_status = sorted(score_status, key=lambda info: info["status"], reverse=True)
    pprint(score_status)

    details = sorted(details, key=lambda detail: detail["level"])
    cnt_by_level = dict()
    for detail in details:
        level = detail["level"]
        if level not in cnt_by_level:
            cnt_by_level[level] = 0
        cnt_by_level[level] += 1

    in_cnt_by_level = dict()
    for i, data in enumerate(score_status):
        level = data["level"]
        # if i < cnt_by_level[level]
