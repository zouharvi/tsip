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

def compute_success(line):
    # fix bad data
    if line["task"] == "reading":
        line["task"] = "questions"
    return (line["times"][1]-line["times"][0])/1000

def perm_distance(A, B):
    return 1-np.average([abs(a_i-B.index(a))/len(A) for a_i, a in enumerate(A)])


data_aggregate = collections.defaultdict(list)
for line in data:
    line["success"] = compute_success(line)

    # fix bad data
    if line["simplification_type"] == "reading":
        line["simplification_type"] = "questions"
        
    data_aggregate[line["simplification_type"]].append(line)


# plotting
plt.figure(figsize=(3.5, 1.5))
succ_questions = []
succ_ordering = []

for key, vals in data_aggregate.items():
    val = np.average([line["success"] for line in vals if line["task"] == "questions"])
    succ_questions.append(val)
for key, vals in data_aggregate.items():
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

plt.bar(
    [x+0.2 for x in range(len(succ_ordering))],
    succ_ordering,
    label="Ordering task",
    **BAR_STYLE
)

plt.xticks(
    range(len(data_aggregate.keys())),
    list(data_aggregate.keys())
)
plt.xlabel("Text simplification model")
plt.ylabel("Task duration (s)   ")

plt.legend(
    loc=(0, 0),
    edgecolor="black", facecolor="white", fancybox=False,
    framealpha=0.9,
    labelspacing=0.2,
    borderpad=0.2,
)

plt.tight_layout(pad=0.1)
# plt.savefig("computed/figures/model_aggregate_time.png", dpi=200)
plt.savefig("computed/figures/model_aggregate_time.pdf")
plt.show()