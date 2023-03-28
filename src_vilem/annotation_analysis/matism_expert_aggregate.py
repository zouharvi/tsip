#!/usr/bin/env python3

import collections
import glob
import json
from scipy.stats import spearmanr
import numpy as np
import jezecek.fig_utils
import matplotlib.pyplot as plt
import scipy.stats as st

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
    # fix bad data
    if line["task"] == "reading":
        line["task"] = "questions"
    if line["task"] == "questions":
        hits = []
        for answer_k, answer_v in line["answers_extrinsic"].items():
            hits.append(line["task_data"][int(answer_k)]["correct"] == answer_v)
        out = np.average(hits)
    elif line["task"] == "ordering":
        out = perm_distance(line["answers_extrinsic"], line["task_data"]["permutation"])
    return out

def perm_distance(A, B):
    return 1-np.average([abs(a_i-B.index(a))/len(A) for a_i, a in enumerate(A)])

def conf_interval(data):
    return st.t.interval(
        confidence=0.90, df=len(data)-1,
        loc=np.mean(data),
        scale=st.sem(data)
    )

data_aggregate = collections.defaultdict(list)
for line in data:
    line["success"] = compute_success(line)

    # fix bad data
    if line["simplification_type"] == "reading":
        line["simplification_type"] = "questions"
        
    data_aggregate[line["simplification_type"]].append(line)

    # normalize data
    if line["task"] == "ordering":
        min_ordering = min(min_ordering, line["success"])
        max_ordering = max(max_ordering, line["success"])
    elif line["task"] == "questions":
        min_questions = min(min_questions, line["success"])
        max_questions = max(max_questions, line["success"])
        
print(min_ordering, max_ordering, min_questions, max_questions)

# aggregation
for line in data:
    if line["task"] == "ordering":
        line["success"] = (line["success"]-min_ordering)/(max_ordering-min_ordering)
    elif line["task"] == "questions":
        line["success"] = (line["success"]-min_questions)/(max_questions-min_questions)

# plotting
plt.figure(figsize=(3.5, 2))
succ_expert = []
succ_nonexpert = []
conf_expert = []
conf_nonexpert = []

for key, val in data_aggregate.items():
    conf_expert.append(conf_interval([line["success"] for line in val if line["url_data"]["level"] == "expert"]))
    val = np.average([line["success"] for line in val if line["url_data"]["level"] == "expert"])
    succ_expert.append(val)
for key, val in data_aggregate.items():
    conf_nonexpert.append(conf_interval([line["success"] for line in val if line["url_data"]["level"] == "nonexpert"]))
    val = np.average([line["success"] for line in val if line["url_data"]["level"] == "nonexpert"])
    succ_nonexpert.append(val)

BAR_STYLE = {
    "width": 0.4,
    "linewidth": 2,
    "edgecolor": "black",
}

plt.bar(
    [x-0.2 for x in range(len(succ_expert))],
    succ_expert,
    label="Expert",
    **BAR_STYLE
)
plt.scatter(
    2*[x-0.2 for x in range(len(conf_expert))],
    [x[0] for x in conf_expert]+[x[1] for x in conf_expert],
    color="black",
    marker="_"
)

plt.bar(
    [x+0.2 for x in range(len(succ_nonexpert))],
    succ_nonexpert,
    label="Nonexpert",
    **BAR_STYLE
)
plt.scatter(
    2*[x+0.2 for x in range(len(conf_nonexpert))],
    [x[0] for x in conf_nonexpert]+[x[1] for x in conf_nonexpert],
    color="black",
    marker="_"
)
plt.xticks(
    range(len(data_aggregate.keys())),
    list(data_aggregate.keys())
)
plt.xlabel("Text simplification model")
plt.ylabel("Task success (overall)")

plt.legend(
    loc="lower left"
)

plt.tight_layout(pad=0)
plt.savefig("computed/figures/expert_aggregate.png", dpi=200)
plt.show()
