import csv
import os
import sys

print(sys.path)

save_dir = "./score/data/note_sims"
save_file_name = "sim_label_318.csv"
os.makedirs(save_dir, exist_ok=True)

with open(f"{save_dir}/{save_file_name}", "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id1", "id2", "label"])

string = """
1,階段
2,階段
7,階段
8,階段
11,階段
12,階段
30,階段
133,階段
157,階段
183,階段
198,階段
249,階段
264,階段
279,階段
280,階段
281,階段
282,階段
283,階段
284,階段
285,階段
287,階段
289,階段
293,階段
295,階段
296,階段
298,階段
300,階段
302,階段
303,階段
310,階段
321,階段
344,階段
364,階段
377,階段
389,階段
401,階段
413,階段
416,階段
421,階段
422,階段
424,階段
426,階段
428,階段
470,階段
482,階段
483,階段
504,階段
"""
ids = [int(s[:-3]) if s[:-3] != "" else None for s in string.split("\n")]
ids = list(filter(lambda x: x is not None, ids))
print(ids)


with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "階段"])


string = """
4,トリル
5,トリル
6,トリル
9,トリル
10,トリル
47,トリル
48,トリル
58,トリル
59,トリル
169,トリル
330,トリル
332,トリル
336,トリル
405,トリル
406,トリル
430,トリル
432,トリル
434,トリル
442,トリル
"""
ids = [int(s[:-4]) if s[:-4] != "" else None for s in string.split("\n")]
ids = list(filter(lambda x: x is not None, ids))
print(ids)


with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "トリル"])


string = """
50,全体階段
51,全体階段
52,全体階段
61,全体階段
62,全体階段
63,全体階段
64,全体階段
210,全体階段
211,全体階段
212,全体階段
213,全体階段
214,全体階段
215,全体階段
"""

ids = [int(s[:-5]) if s[:-5] != "" else None for s in string.split("\n")]
ids = list(filter(lambda x: x is not None, ids))
print(ids)


with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "階段"])


string = """
233,全体トリル
255,全体トリル
237,全体トリル
239,全体トリル
266,全体トリル
268,全体トリル
270,全体トリル
272,全体トリル
"""

ids = [int(s[:-6]) if s[:-6] != "" else None for s in string.split("\n")]
ids = list(filter(lambda x: x is not None, ids))
print(ids)


with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "トリル"])


ids = [207, 208, 209]
with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "階段"])

ids = [402, 403, 414, 415, 509]
with open(f"{save_dir}/{save_file_name}", "a", newline="") as f:
    writer = csv.writer(f)
    for i in range(len(ids)):
        for j in range(i + 1, len(ids)):
            writer.writerow([ids[i], ids[j], "階段，トリル"])
