import constant

judge_types = {
    0: "off",
    1: "flick_up",
    2: "flick_down",
    3: "flick_left",
    4: "flick_right",
    5: "push",
    6: "hold",
}
target = {
    i: x for x, i in zip(constant.JUDGLE_TYPES, range(len(constant.JUDGLE_TYPES)))
}

assert judge_types == target, "not same"
print(target)
print(judge_types)
print(target[0])
