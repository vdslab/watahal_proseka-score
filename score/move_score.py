from collections import defaultdict
from functools import reduce
from pprint import pprint

from classes import FingeringHand, Note
from classes.types import HoldType, JudgeType, NotesType
from constant import CONTINUOUS_COST_RATE, MAX_KEYBOARD_COUNT, PUSHED_COST
from section_divide import _get_section, get_section


def get_move_dist_cost(hand: FingeringHand, note: Note):
    cost = abs(hand.x - note.x)
    return cost if hand.can_push(note) else PUSHED_COST


def get_continuous_index_count(list_index: list[int]):
    if list_index is None or len(list_index) == 0:
        return 0

    now = list_index[0]
    cnt = 0
    for id in list_index:
        if id != now:
            break

        now += 1
        cnt += 1

    return cnt


def get_continuous_cost(hand: FingeringHand, note: Note, note_index: int):
    move_cost = get_move_dist_cost(hand, note)
    hand_notes_index, hand_notes = hand.notes

    notes_contain_item = hand_notes is not None and len(hand_notes) > 0
    is_continue = notes_contain_item and hand_notes_index[-1] == note_index - 1
    continue_cnt = get_continuous_index_count(hand_notes_index)

    cost = (
        move_cost * (CONTINUOUS_COST_RATE**continue_cnt) if is_continue else move_cost
    )
    return cost


def get_cost(hand: FingeringHand, note: Note, note_index: int):
    move_dist_cost = get_move_dist_cost(hand, note)
    continuous_cost = get_continuous_cost(hand, note, note_index)
    return sum([move_dist_cost, continuous_cost])


def get_lr_fingering(
    notes_index_by_y: dict[float, list]
) -> tuple[FingeringHand, FingeringHand]:
    """Return left and right fingering by one sections"""
    left = FingeringHand()
    right = FingeringHand(x=MAX_KEYBOARD_COUNT)
    # 運指の作成
    for i, note in enumerate(notes_index_by_y.values()):
        print(f"{note=}")
        left_cost = get_cost(left, note, i)
        right_cost = get_cost(right, note, i)
        if left_cost <= right_cost:
            left.add_notes((i, note))
            left.add_cost(left_cost)
        else:
            right.add_notes((i, note))
            right.add_cost(right_cost)

    return left, right


def _get_fingering(
    notes_json_file_relative_path: str,
) -> list[dict[str, FingeringHand]]:
    notes_section = _get_section(notes_json_file_relative_path)
    fingering: list[dict[str, FingeringHand]] = []

    for i, section in enumerate(notes_section):
        # y座標ごとのノーツIDを格納
        # 中間点は削除
        notes_index_by_y = defaultdict(list[int])
        for i, note in enumerate(section):
            if note.hold_type == HoldType.MIDDLE:
                continue
            notes_index_by_y[note.y].append(i)
        # for i, note in enumerate(notes_index_by_y.items()):
        #     print(i, note)

        # 左右の運指
        left, right = get_lr_fingering(notes_index_by_y)
        fingering.append({"left": left, "right": right})
    return fingering


def _get_lr_fingering(section, notes_index_by_y: dict[float, list]):
    # 左右の運指
    left = FingeringHand()
    right = FingeringHand(x=MAX_KEYBOARD_COUNT)
    left_dict = {"x": 0, "notes": [], "cost": 0, "pushing": False}
    right_dict = {
        "x": MAX_KEYBOARD_COUNT,
        "notes": [],
        "cost": 0,
        "pushing": False,
    }

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
            update_hand_from_index(section, left_dict, left_note_index)

            right_note_index = note[1][1]
            update_hand_from_index(section, right_dict, right_note_index)
        else:
            # 移動距離をそれぞれ求めて，小さい方で取る
            note_index = note[1][0]
            left_move = abs(left_dict["x"] - section[note_index]["x"])
            right_move = abs(right_dict["x"] - section[note_index]["x"])

            if left_move <= right_move:
                if can_push_note(left_dict, note_index):
                    update_hand_from_index(section, left_dict, note_index)
                else:
                    update_hand_from_index(section, right_dict, note_index)
            else:
                if can_push_note(left_dict, note_index):
                    update_hand_from_index(section, right_dict, note_index)
                else:
                    update_hand_from_index(section, left_dict, note_index)

    return left_dict, right_dict


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
        # break
        # ---
    return fingering


def main():
    pprint(_get_fingering("score/data/m155_notes-test.json"))


if __name__ == "__main__":
    main()

    test_note = Note(x=3, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF)
    test_note2 = Note(x=3, y=5, width=3, type=NotesType.HOLD, judge_type=JudgeType.HOLD)
    assert get_move_dist_cost(FingeringHand(), test_note) == 3

    test_hand = FingeringHand()
    test_hand.pushing = True
    assert get_move_dist_cost(test_hand, test_note) == PUSHED_COST

    ids = [1, 2, 3, 4, 5]
    assert get_continuous_index_count(ids) == 5

    test_hand = FingeringHand()
    test_notes = [
        Note(x=3, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF),
        Note(x=4, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF),
        Note(x=5, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF),
        Note(x=6, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF),
        Note(x=7, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF),
    ]
    test_add_note = Note(
        x=8, y=5, width=3, type=NotesType.NORMAL, judge_type=JudgeType.OFF
    )
    for v in zip(range(len(test_notes)), test_notes):
        test_hand.add_notes(v)

    assert (
        abs(get_continuous_cost(test_hand, test_add_note, len(test_notes)) - 2.48832)
        < 0.000_01
    )
