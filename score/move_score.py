from collections import defaultdict
from functools import reduce
from pprint import pprint

import constant
from section_divide import get_section


def _get_lr_fingering(section, notes_index_by_y):
    # 左右の運指
    left = {"x": 0, "notes": [], "cost": 0, "pushing": False}
    right = {
        "x": constant.MAX_KEYBOAD_COUNT,
        "notes": [],
        "cost": 0,
        "pushing": False,
    }

    PUSHED_COST = 100
    CONTINUOUS_COST_RATE = 1.2

    def get_move_dist_cost(hand: dict, note_index: int):
        cost = abs(hand["x"] - section[note_index]["x"])
        return cost if can_push_note(hand, note_index) else PUSHED_COST

    def get_continuous_cost(hand: dict, note_index: int):
        move_cost = get_move_dist_cost(hand, note_index)
        is_continue = len(hand["notes"]) > 0 and hand["notes"][-1] == note_index - 1

        def reduce_func(x, y):
            is_continue = x + 1 < len(hand["notes"]) and hand["notes"][x + 1] == y + 1
            cnt = x + 1 if is_continue else x
            return cnt + 1 if y == hand["notes"][-1] else cnt

        continue_cnt = reduce(reduce_func, hand["notes"][::-1], 0)
        cost = (
            move_cost * (CONTINUOUS_COST_RATE**continue_cnt)
            if is_continue
            else move_cost
        )
        return cost

    def get_cost(hand: dict, note_index: int):
        push_note = section[note_index]
        move_dist_cost = get_move_dist_cost(hand, note_index)
        continuous_cost = get_continuous_cost(hand, note_index)

    def can_push_note(hand: dict, note_index: int):
        push_note = section[note_index]
        if hand["pushing"]:
            if push_note["judge_type"] == "hold" and push_note["hold_type"] == "end":
                return True

            return False

        return True

    def update_hand_from_index(
        section: list[list[dict]], hand: dict, note_index: int
    ) -> dict:
        push_note = section[note_index]
        hand["notes"].append(note_index)
        hand["cost"] += abs(hand["x"] - push_note["x"])
        hand["x"] = push_note["x"]
        if push_note["hold_type"] == "end":
            hand["pushing"] = False
        else:
            hand["pushing"] = True

    # 運指の作成
    for note in notes_index_by_y.items():
        if len(note[1]) >= 2:
            # 単純に左右にある方をそれぞれに追加
            left_note_index = note[1][0]
            update_hand_from_index(section, left, left_note_index)

            right_note_index = note[1][1]
            update_hand_from_index(section, right, right_note_index)
        else:
            # 移動距離をそれぞれ求めて，小さい方で取る
            note_index = note[1][0]
            left_move = abs(left["x"] - section[note_index]["x"])
            right_move = abs(right["x"] - section[note_index]["x"])

            if left_move <= right_move:
                if can_push_note(left, note_index):
                    update_hand_from_index(section, left, note_index)
                else:
                    update_hand_from_index(section, right, note_index)
            else:
                if can_push_note(left, note_index):
                    update_hand_from_index(section, right, note_index)
                else:
                    update_hand_from_index(section, left, note_index)

    return left, right


def get_fingering(notes_json_file_relative_path: str) -> list[dict]:
    """
    同時押しと同時押しの区間において，運指を，左右どちらでとるかを移動距離ベースで作成する

    ただしノーツは，ホールドの中間点を除いている

    優先順位：左の座標と近いノーツ，左手

    # Returns
    fingering = { "left" : array, "right" : array }
    """

    notes_section = get_section(notes_json_file_relative_path)
    fingering: list[dict] = []

    for i, section in enumerate(notes_section):
        # --- デバッグ用の区間調整
        # if i < 3:
        #     continue
        # if i >= 8:
        #     break
        # ---
        # print(section)
        # y座標ごとのノーツIDを格納
        # 中間点は削除
        notes_index_by_y = defaultdict(list[int])
        for i, note in enumerate(section):
            if note["hold_type"] == "middle":
                continue
            notes_index_by_y[note["y"]].append(i)
        # for i, note in enumerate(notes_index_by_y.items()):
        #     print(i, note)

        # 左右の運指
        left, right = _get_lr_fingering(section, notes_index_by_y)
        fingering.append({"left": left, "right": right})

        # --- デバッグ用
        # 出力確認
        # print("i:", i)
        # print("left")
        # print(left)
        # print("right")
        # print(right)
        # print()
        # 区間調整
        # if i >= 64:
        break
        # ---
    return fingering


def main():
    get_fingering("score/data/m155_notes.json")


if __name__ == "__main__":
    main()
