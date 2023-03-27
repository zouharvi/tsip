#!/usr/bin/env python3

import argparse
import json
from mi_library import add_all
from load_data import load_corpus

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="computed/onestopqa_tsip_dataset.jsonl"
)
args.add_argument(
    "-o", "--output", default="computed/onestopqa_tsip_dataset_mi.jsonl"
)
args = args.parse_args()

data, _ = load_corpus(input=args.input)
data = [x | {"mi": {}} for x in data]

add_all(data)

with open(args.output, "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False) + "\n")
