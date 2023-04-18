# [y座標(中央),
# (1:通常orフリック/3:ロングノーツ),
# 2個以上ホールがあるときの識別用？,
# (1:ホールド始点/2:ホールド終点/3:ホールド中間判定),
# 黄色ノーツか否か(1or2),
# (1:フリック(はじく)/3 flick left /4 flick right/5:ホールド始点(押し続ける)/6:ホールド中間判定(押しっぱなし)/0:ホールド終端or通常(離す)),
# x座標(左端),
# 幅]

import json
from pprint import pprint

# _bpms = None
# _fever = None
# _skills = None

notes: list[dict] = []
notes_explain = [
    "y",
    "type",
    "hole",
    "hold_type",
    "is_yellow",
    "judge_type",
    "x",
    "width",
]
judge_types = {
    0: "off",
    1: "flick",
    3: "flick_left",
    4: "flick_right",
    5: "push",
    6: "hold",
}
hold_types = {0: "none", 1: "start", 2: "end", 3: "middle"}
types = {1: "normal", 3: "long"}
_score = None
with open("score/sample_score.json", "r") as f:
    _score = json.load(f)

for _note in _score["notes"]:
    note = dict()
    # print(_note)
    # print(notes_explain)
    for n, key in zip(_note, notes_explain):
        if key == "is_yellow":
            note[key] = n != 1
        elif key == "judge_type":
            note[key] = judge_types[n]
        elif key == "hold_type":
            note[key] = hold_types[n]
        elif key == "type":
            note[key] = types[n]
        else:
            note[key] = n
    # print(note)
    notes.append(note)

# pprint(notes[:10])


# score = dict()
with open("score/sample_score_notes_m282.json", "w") as f:
    json.dump(notes, f, indent=2, ensure_ascii=False)
