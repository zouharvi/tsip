#!/usr/bin/env python3

import collections
import json
import glob
import numpy as np

def load_raw(input_globs=["data/collected/**/*.jsonl", "data/collected/*.jsonl"]):
    data_flat = []
    data_pid = {}

    for input_glob in input_globs:
        for fname in glob.glob(input_glob):
            with open(fname, "r") as f:
                data_local = [json.loads(x) for x in f.readlines()]
                identifier = data_local[0]["uid"]
                if "prolific_pid" in data_local[0]:
                    identifier += "-" + data_local[0]["prolific_pid"]
                data_pid[identifier] = data_local
                data_flat += data_local

    for pid, data_local in data_pid.items():
        print(pid)
        times_total = []
        times_total_i = collections.defaultdict(list)
        for line in data_local:
            seconds_total = (line["times"][-1] - line["times"][0]) / 1000
            line["time_total"] = seconds_total
            times_total.append(seconds_total)

            for i in [1, 2, 3]:
                seconds_i = (
                    line["times"][i] - line["times"][i - 1]
                ) / 1000
                line[f"time_{i}"] = seconds_i
                times_total_i[i].append(seconds_i)

        time_avg = np.average(times_total)
        time_avg_i = {i:np.average(x) for i,x in times_total_i.items()}

        for line in data_local:
            line["time_total_norm"] = (
                line["times"][-1] - line["times"][0]
            ) / 1000 - time_avg

            for i in [1, 2, 3]:
                seconds_i = (
                    line["times"][i] - line["times"][i - 1]
                ) / 1000
                line[f"time_{i}_norm"] = seconds_i - time_avg_i[i]

    data_modes = collections.defaultdict(list)
    for line in data_flat:
        data_modes[line["mode"]].append(line)

    # "How confident are you in your answers?",
    # "Did the text provide enough information to answer the questions?",
    # "Did the text contain only necessary information?",
    # "What is the complexity of the text?",
    # "What is the fluency & grammaticality of the text?",

    return data_flat, data_modes

def load_corpus(
    input="computed/onestopqa_tsip_dataset_mi.jsonl"
):
    with open(input, "r") as f:
        data_flat = [json.loads(l) for l in f.readlines()]

    data_modes = collections.defaultdict(list)
    for line in data_flat:
        data_modes[line["mode"]].append(line)

    return data_flat, data_modes