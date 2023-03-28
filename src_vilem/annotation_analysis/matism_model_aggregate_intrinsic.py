#!/usr/bin/env python3

import collections
import glob
import json
import numpy as np
import scipy.stats as st
import jezecek.fig_utils
import matplotlib.pyplot as plt

data = [
    json.loads(x)
    for f in glob.glob("data_matism/collected/*.jsonl")
    for x in open(f, "r").readlines()
]

def compute_success(line):
    # fix bad data
    if line["task"] == "reading":
        line["task"] = "questions"
    return line["answers_intrinsic"]

data_aggregate = collections.defaultdict(list)
for line in data:
    line["success"] = compute_success(line)

    # fix bad data
    if line["simplification_type"] == "reading":
        line["simplification_type"] = "questions"
        
    data_aggregate[line["simplification_type"]].append(line)

# plotting
plt.figure(figsize=(3.5, 2))
succ_confidence = []
conf_confidence = []
succ_complexity = []
conf_complexity = []
succ_fluency = []
conf_fluency = []

def conf_interval(data):
    return st.t.interval(
        confidence=0.90, df=len(data)-1,
        loc=np.mean(data),
        scale=st.sem(data)
    )

for key, val in data_aggregate.items():
    succ_confidence.append(np.average([line["success"]["confidence"] for line in val]))
    conf_confidence.append(conf_interval([line["success"]["confidence"] for line in val]))
    succ_complexity.append(np.average([line["success"]["complexity"] for line in val]))
    conf_complexity.append(conf_interval([line["success"]["complexity"] for line in val]))
    succ_fluency.append(np.average([line["success"]["fluency"] for line in val]))
    conf_fluency.append(conf_interval([line["success"]["fluency"] for line in val]))

BAR_STYLE = {
    "width": 0.3,
    "linewidth": 2,
    "edgecolor": "black",
}

plt.bar(
    [x-0.3 for x in range(len(succ_confidence))],
    succ_confidence,
    label="Confidence",
    **BAR_STYLE
)
plt.scatter(
    2*[x-0.3 for x in range(len(succ_confidence))],
    [x[0] for x in conf_confidence]+[x[1] for x in conf_confidence],
    color="black",
    marker="_"
)

plt.bar(
    [x for x in range(len(succ_complexity))],
    succ_complexity,
    label="Complexity",
    **BAR_STYLE
)
plt.scatter(
    2*[x for x in range(len(succ_confidence))],
    [x[0] for x in conf_complexity]+[x[1] for x in conf_complexity],
    color="black",
    marker="_"
)

plt.bar(
    [x+0.3 for x in range(len(succ_fluency))],
    succ_fluency,
    label="Fluency",
    **BAR_STYLE
)
plt.scatter(
    2*[x+0.3 for x in range(len(succ_confidence))],
    [x[0] for x in conf_fluency]+[x[1] for x in conf_fluency],
    color="black",
    marker="_"
)

plt.xticks(
    range(len(data_aggregate.keys())),
    list(data_aggregate.keys())
)
plt.xlabel("Text simplification model")
plt.ylabel("Human annotation")

plt.legend(
    loc="lower left"
)

plt.tight_layout(pad=0)
plt.savefig("computed/figures/model_aggregate_intrinsic.png", dpi=200)
plt.show()