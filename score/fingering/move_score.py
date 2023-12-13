import glob
import json
import os
import pprint
import re
import sys
from collections import defaultdict

from classes import FingeringHand, Note
from classes.types import HoldType

# from classes.types import HoldType, JudgeType, NotesType
from constant import CONTINUOUS_COST_RATE, MAX_KEYBOARD_COUNT, PUSHED_COST
from section_divide import _get_section


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


def insert_note_to_hand(hand: FingeringHand, note: Note, note_index: int):
    left_cost = get_cost(hand, note, note_index)
    hand.add_notes((note_index, note))
    hand.add_cost(left_cost)
    return hand


def get_lr_fingering(
    id_and_notes_by_y: dict[float, list[tuple[int, Note]]], first: bool
) -> tuple[FingeringHand, FingeringHand]:
    """Return left and right fingering by one sections"""
    left = FingeringHand()
    right = FingeringHand(x=MAX_KEYBOARD_COUNT)
    sorted_id_and_notes_by_y = sorted(id_and_notes_by_y.items(), key=lambda x: x[0])
    # 運指の作成
    for i, (y, notes) in enumerate(sorted_id_and_notes_by_y):
        if not first and i == 0:
            continue

        if len(notes) > 2:
            # cprint("\tノーツが3つ以上．いったん端っこだけ取る", attrs=[Color.GREEN])
            # notes.sort(key=lambda x: x[1].x)
            # for i, note in notes:
            #     if i < len(notes) // 2:
            #         left = insert_note_to_hand(left, note, i)
            #     else:
            #         right = insert_note_to_hand(right, note, i)
            edge_notes = [notes[0], notes[-1]]
            ((l_id, l_note), (r_id, r_note)) = (
                (edge_notes[0], edge_notes[1])
                if edge_notes[0][1].x < edge_notes[1][1].x
                else (edge_notes[1], edge_notes[0])
            )
            if left.can_push(l_note):
                insert_note_to_hand(left, l_note, l_id)
                insert_note_to_hand(right, r_note, r_id)
            else:
                insert_note_to_hand(left, r_note, r_id)
                insert_note_to_hand(right, l_note, l_id)
            continue

        if len(notes) == 2:
            ((l_id, l_note), (r_id, r_note)) = (
                (notes[0], notes[1])
                if notes[0][1].x < notes[1][1].x
                else (notes[1], notes[0])
            )
            if left.can_push(l_note):
                insert_note_to_hand(left, l_note, l_id)
                insert_note_to_hand(right, r_note, r_id)
            else:
                insert_note_to_hand(left, r_note, r_id)
                insert_note_to_hand(right, l_note, l_id)
            continue

        (id, note) = notes[0]
        if note.is_hold and (left.pushing or right.pushing):
            if left.pushing and left.can_push(note):
                insert_note_to_hand(left, note, id)
            elif right.pushing and right.can_push(note):
                insert_note_to_hand(right, note, id)
            continue

        left_cost = get_cost(left, note, id)
        right_cost = get_cost(right, note, id)
        if left_cost <= right_cost:
            insert_note_to_hand(left, note, id)
        else:
            insert_note_to_hand(right, note, id)

    return left, right


def _get_fingering(
    notes_json_file_relative_path: str,
) -> list[dict[str, FingeringHand]]:
    notes_section = _get_section(notes_json_file_relative_path)
    fingering: list[dict[str, FingeringHand]] = []

    for i, section in enumerate(notes_section):
        # y座標ごとのノーツIDを格納
        id_and_notes_by_y: dict[float, list[tuple[int, Note]]] = defaultdict(
            list[tuple[int, Note]]
        )
        for j, note in enumerate(section):
            id_and_notes_by_y[note.y].append((j, note))
        # 左右の運指
        left, right = get_lr_fingering(id_and_notes_by_y, i == 0)

        fingering.append({"left": left, "right": right})
    return fingering


def get_fingering(path: str):
    fingering = _get_fingering(path)
    left_notes = []
    right_notes = []
    for f in fingering:
        _, l_notes = f["left"].notes
        _, r_notes = f["right"].notes
        if l_notes is None:
            l_notes = []
        if r_notes is None:
            r_notes = []

        left_notes += [note.to_dict() for note in l_notes]
        right_notes += [note.to_dict() for note in r_notes]

    def unique(notes):
        jsonize = [json.dumps(d, sort_keys=True) for d in notes]
        set_json = list(dict.fromkeys(jsonize))
        set_notes = [json.loads(d) for d in set_json]
        return set_notes

    fingering_dict = {"left": unique(left_notes), "right": unique(right_notes)}
    return fingering_dict


def main():
    file_paths = glob.glob("./proseka/datas/*.json")
    file_paths = sorted(
        file_paths, key=lambda path: int(re.search(r"\d+", path).group())
    )
    save_dir = "./score/data/_json/1030/fingering"
    os.makedirs(save_dir, exist_ok=True)
    for path in file_paths[:1]:
        fingering_dict = get_fingering(path)

        # check notes count
        fingering_notes_count = len(fingering_dict["left"]) + len(
            fingering_dict["right"]
        )
        data_notes_count = 0
        id = int(re.search(r"\d+", path).group())
        with open(f"score/data/notes_score/score-{id}.json", "r") as f:
            notes = json.load(f)
            notes = list(filter(lambda note: note["hold_type"] != "middle", notes))
            data_notes_count = len(notes)

        assert (
            fingering_notes_count == data_notes_count
        ), f"{fingering_notes_count=}, {data_notes_count=}"

        name = os.path.splitext(os.path.basename(path))[0]
        with open(f"{save_dir}/{name}.json", "w", newline="") as f:
            json.dump(fingering_dict, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
