#!/usr/bin/env python3

import collections
import glob
import json
from scipy.stats import spearmanr
import numpy as np

data = [
    json.loads(x)
    for f in glob.glob("data_matism/collected/*.jsonl")
    for x in open(f, "r").readlines()
]

min_ordering = 1
max_ordering = 0
min_questions = 1
max_questions = 0

def compute_success(line):
    global min_ordering
    global max_ordering, min_questions, max_questions
    if line["task"] == "reading":
        hits = []
        for answer_k, answer_v in line["answers_extrinsic"].items():
            hits.append(line["task_data"][int(answer_k)]["correct"] == answer_v)
        out = np.average(hits)
    elif line["task"] == "ordering":
        out = perm_distance(line["answers_extrinsic"], line["task_data"]["permutation"])
    return out

def perm_distance(A, B):
    return 1-np.average([abs(a_i-B.index(a))/len(A) for a_i, a in enumerate(A)])

data_aggregate = collections.defaultdict(list)
for line in data:
    line["success"] = compute_success(line)

    # fix bad data
    if line["simplification_type"] == "reading":
        line["simplification_type"] = "questions"
        
    data_aggregate[line["simplification_type"]].append(line)

    if line["task"] == "ordering":
        min_ordering = min(min_ordering, line["success"])
        max_ordering = max(max_ordering, line["success"])
    elif line["task"] == "questions":
        min_questions = min(min_questions, line["success"])
        max_questions = max(max_questions, line["success"])
        
# TODO: normalize data
print(min_ordering, max_ordering, min_questions, max_questions)

for line in data:
    if line["task"] == "ordering":
        line["success"] = (line["success"]-min_ordering)/(max_ordering-min_ordering)
    elif line["task"] == "questions":
        line["success"] = (line["success"]-min_questions)/(max_questions-min_questions)


for task_type in ["reading", "ordering"]:
    print("\n", task_type)
    for key, val in data_aggregate.items():
        print(key, np.average([line["success"] for line in val if line["task"] == task_type]))

print()

for level_type in ["expert", "nonexpert"]:
    print("\n", level_type)
    for key, val in data_aggregate.items():
        print(key, np.average([line["success"] for line in val if line["url_data"]["level"] == level_type]))