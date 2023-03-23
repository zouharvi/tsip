#!/usr/bin/env python3

import json
import argparse
import glob

args = argparse.ArgumentParser()
args.add_argument("-ie", "--input-extraction", default="computed/onestopqa_extraction.jsonl")
args.add_argument("-ig", "--input-glob", default="computed/onestopqa_simplified/*/*.jsonl")
args.add_argument("-o", "--output", default="computed/onestopqa_extraction_all.jsonl")
args = args.parse_args()

with open(args.input_extraction, "r") as f:
    data = [json.loads(x) for x in f.readlines()]

for fname in glob.glob(args.input_glob):
    with open(fname, "r") as f:
        data_local = [json.loads(x) for x in f.readlines()]
        data_local = {x["id"]: x["text"]["machine_simple"] for x in data_local}
    
    machine_name = fname.split("/")[-1].removesuffix(".jsonl").removeprefix("onestopqa_")
    for line in data:
        line["text"][machine_name] = data_local[line["id"]]

with open(args.output, "w") as f:
    for line in data:
        f.write(json.dumps(line, ensure_ascii=False)+"\n")