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
plt.figure(figsize=(3.5, 1.5))
succ_questions = []
succ_ordering = []
conf_questions = []
conf_ordering = []

for key, vals in data_aggregate.items():
    conf_questions.append(conf_interval([line["success"] for line in vals if line["task"] == "questions"]))
    val = np.average([line["success"] for line in vals if line["task"] == "questions"])
    succ_questions.append(val)
for key, vals in data_aggregate.items():
    conf_ordering.append(conf_interval([line["success"] for line in vals if line["task"] == "ordering"]))
    val = np.average([line["success"] for line in vals if line["task"] == "ordering"])
    succ_ordering.append(val)

BAR_STYLE = {
    "width": 0.4,
    "linewidth": 2,
    "edgecolor": "black",
}

plt.bar(
    [x-0.2 for x in range(len(succ_questions))],
    succ_questions,
    label="Questions task",
    **BAR_STYLE
)
plt.scatter(
    2*[x-0.2 for x in range(len(succ_questions))],
    [x[0] for x in conf_questions]+[x[1] for x in conf_questions],
    color="black",
    marker="_"
)

plt.bar(
    [x+0.2 for x in range(len(succ_ordering))],
    succ_ordering,
    label="Ordering task",
    **BAR_STYLE
)
plt.scatter(
    2*[x+0.2 for x in range(len(succ_questions))],
    [x[0] for x in conf_ordering]+[x[1] for x in conf_ordering],
    color="black",
    marker="_"
)

plt.ylim(0, 1)

plt.xticks(
    range(len(data_aggregate.keys())),
    list(data_aggregate.keys())
)
plt.xlabel("Text simplification model")
plt.ylabel("Task success")

plt.legend(
    loc=(0, 0),
    edgecolor="black", facecolor="white", fancybox=False,
    framealpha=0.9,
    labelspacing=0.2,
    borderpad=0.2,
)

plt.tight_layout(pad=0)
# plt.savefig("computed/figures/model_aggregate.png", dpi=200)
plt.savefig("computed/figures/model_aggregate.pdf")
plt.show()