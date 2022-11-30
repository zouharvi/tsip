#!/usr/bin/env python3

import collections
import json
import argparse
import glob
import operator

import numpy as np

args = argparse.ArgumentParser()
args.add_argument("-ig", "--input-glob", default="data/collected/*.jsonl")
args = args.parse_args()

data_flat = []
data_uid = {}

for fname in glob.glob(args.input_glob):
    with open(fname, "r") as f:
        data_local = [json.loads(x) for x in f.readlines()]
        data_uid[data_local[0]["uid"]] = data_local
        data_flat += data_local

for uid, data_local in data_uid.items():
    print(uid)
    times_total = []
    for line in data_local:
        seconds_total = (line["times"][-1]-line["times"][0])/1000
        times_total.append(seconds_total)
    print(f"Time total:   {sum(times_total)/60:.1f}m")
    print(f"Time average: {np.average(times_total):.1f}s")

data_modes = collections.defaultdict(list)
for line in data_flat:
    data_modes[line["mode"]].append(line)

data = []

for mode, data_local in data_modes.items():
    avg_correct = np.average([[v == 0 for v in line["answers_extrinsic"].values()] for line in data_local])
    avg_intrinsic = [
        np.average([line["answers_intrinsic"][f"{i}"] for line in data_local])
        for i in range(5)
    ]

    times_total = []
    for line in data_local:
        seconds_total = (line["times"][-1]-line["times"][0])/1000
        times_total.append(seconds_total)

    avg_intrinsic_text = " ".join([f"{v:.1f}" for v in avg_intrinsic])
    data.append((mode, avg_correct, avg_intrinsic_text, np.average(times_total)))

data.sort(key=operator.itemgetter(1))

for mode, avg_correct, avg_intrinsic_text, times_avg in data:
    print(f"{mode:>30}: {avg_correct:>4.0%} acc {times_avg:>3.0f}s {avg_intrinsic_text}")

# "How confident are you in your answers?",
# "Did the text provide enough information to answer the questions?",
# "Did the text contain only necessary information?",
# "What is the complexity of the text?",
# "What is the fluency & grammaticality of the text?",
