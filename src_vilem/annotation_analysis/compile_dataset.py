#!/usr/bin/env python3

import argparse
import load_data
import numpy as np
import json

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="computed/onestopqa_extraction_all.jsonl"
)
args.add_argument(
    "-o", "--output", default="computed/onestopqa_tsip_dataset.jsonl"
)
args = args.parse_args()

with open(args.input, "r") as f:
    data = [json.loads(l) for l in f.readlines()]

    # flatten and merge together
    # don't do this at home
    data = {
        (line["id"], mode):
        line | {
            "mode": mode,
            "text_human": line["text"]["original"],
            "text_human_simple": line["text"]["human_simple"],
            "text_system": text,
            "hihe": []
        } for line in data
        for mode, text in line["text"].items()
    }
    for line in data.values():
        del line["text"]

data_flat, data_modes = load_data.load_raw()

for line in data_flat:
    id = line.pop("id")
    mode = line.pop("mode")
    data[(id, mode)]["hihe"].append(line)

# reorganize and turn into list
data = [
    {"id": line["id"], "mode": line["mode"]} | line
    for line in data.values()
]

with open(args.output, "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
