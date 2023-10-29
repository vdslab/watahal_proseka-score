import glob
import json
import os
from collections import defaultdict

from classes import FingeringHand, Note
from classes.types import HoldType, JudgeType, NotesType
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


def get_lr_fingering(
    id_and_notes_by_y: dict[float, list[tuple[int, Note]]]
) -> tuple[FingeringHand, FingeringHand]:
    """Return left and right fingering by one sections"""
    left = FingeringHand()
    right = FingeringHand(x=MAX_KEYBOARD_COUNT)
    # 運指の作成
    for i, notes in enumerate(id_and_notes_by_y.values()):
        if len(notes) > 2:
            notes.sort(key=lambda x: x[1].x)
            for i, note in notes:
                if i < len(notes) // 2:
                    left_cost = get_cost(left, note, i)
                    left.add_notes((i, note))
                    left.add_cost(left_cost)
                else:
                    right_cost = get_cost(right, note, i)
                    right.add_notes((i, note))
                    right.add_cost(right_cost)
            continue

        if len(notes) == 2:
            ((l_id, l_note), (r_id, r_note)) = (
                (notes[0], notes[1])
                if notes[0][1].x < notes[1][1].x
                else (notes[1], notes[0])
            )
            # left
            left_cost = get_cost(left, l_note, l_id)
            left.add_notes((l_id, l_note))
            left.add_cost(left_cost)
            # right
            right_cost = get_cost(right, r_note, r_id)
            right.add_notes((r_id, r_note))
            right.add_cost(right_cost)
            continue
        # print(f"{notes=}")
        (id, note) = notes[0]
        if note.is_hold:
            _, l_notes = left.notes
            _, r_notes = right.notes
            if left.pushing and l_notes[-1].hole == note.hole:
                left_cost = get_cost(left, note, id)
                left.add_notes((id, note))
                continue

            if right.pushing and r_notes[-1].hole == note.hole:
                right_cost = get_cost(right, note, id)
                right.add_notes((id, note))
                continue

            print("[TODO] ホールドが3つ以上")

        left_cost = get_cost(left, note, id)
        right_cost = get_cost(right, note, id)
        if left_cost <= right_cost:
            left.add_notes((id, note))
            left.add_cost(left_cost)
        else:
            right.add_notes((id, note))
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
        id_and_notes_by_y: dict[float, list[tuple[int, Note]]] = defaultdict(
            list[tuple[int, Note]]
        )
        for i, note in enumerate(section):
            if note.hold_type == HoldType.MIDDLE:
                continue
            id_and_notes_by_y[note.y].append((i, note))
        # for i, note in enumerate(notes_index_by_y.items()):
        #     print(i, note)
        # print(f"{id_and_notes_by_y=}")

        # 左右の運指
        left, right = get_lr_fingering(id_and_notes_by_y)
        fingering.append({"left": left, "right": right})
    return fingering


def main():
    file_paths = glob.glob("./proseka/datas/*.json")
    save_dir = "./score/data/_json/1030/fingering"
    os.makedirs(save_dir, exist_ok=True)
    for path in file_paths[:1]:
        fingering = _get_fingering(path)
        left_notes = []
        right_notes = []
        for f in fingering:
            _, l_notes = f["left"].notes
            _, r_notes = f["right"].notes
            if l_notes is None or r_notes is None:
                print(path)
                continue

            left_notes += [note.to_dict() for note in l_notes]
            right_notes += [note.to_dict() for note in r_notes]

        def unique(notes):
            jsonize = [json.dumps(d, sort_keys=True) for d in notes]
            set_json = list(dict.fromkeys(jsonize))
            set_notes = [json.loads(d) for d in set_json]
            return set_notes

        fingering_dict = {"left": unique(left_notes), "right": unique(right_notes)}

        name = os.path.splitext(os.path.basename(path))[0]
        with open(f"{save_dir}/{name}.json", "w", newline="") as f:
            json.dump(fingering_dict, f, indent=2, ensure_ascii=False)


if __name__ == "__main__":
    main()
