#!/usr/bin/env python3

import collections
import json
import glob
import numpy as np

def load_raw(input_globs=["data/collected/**/*.jsonl", "data/collected/*.jsonl"]):
    data_flat = []
    data_uid = {}

    for input_glob in input_globs:
        for fname in glob.glob(input_glob):
            with open(fname, "r") as f:
                data_local = [json.loads(x) for x in f.readlines()]
                data_uid[data_local[0]["uid"]] = data_local
                data_flat += data_local

    for uid, data_local in data_uid.items():
        print(uid)
        times_total = []
        for line in data_local:
            seconds_total = (line["times"][-1] - line["times"][0]) / 1000
            times_total.append(seconds_total)

        time_avg = np.average(times_total)
        for line in data_local:
            line["time_all_norm"] = (
                line["times"][-1] - line["times"][0]) / 1000 - time_avg
            line["time_all"] = (line["times"][-1] - line["times"][0]) / 1000

            for i in [1, 2, 3]:
                line[f"time_{i}"] = (
                    line["times"][i] - line["times"][i - 1]
                ) / 1000

    data_modes = collections.defaultdict(list)
    for line in data_flat:
        data_modes[line["mode"]].append(line)

    # "How confident are you in your answers?",
    # "Did the text provide enough information to answer the questions?",
    # "Did the text contain only necessary information?",
    # "What is the complexity of the text?",
    # "What is the fluency & grammaticality of the text?",

    return data_flat, data_modes
