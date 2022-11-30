#!/usr/bin/env python3

import copy
import sys
sys.path.append("src_vilem")
import argparse
import json
import random

args = argparse.ArgumentParser()
args.add_argument(
    "-i", "--input", default="computed/onestopqa_extraction_all.jsonl"
)
args.add_argument(
    "-o", "--output", default="src_annotation_ui/web/queues/prolific_onestopqa_pilot_1/sUID.jsonl"
)
args = args.parse_args()

random.seed(0)

with open(args.input, "r") as f:
    data = [json.loads(l) for l in f.readlines()]

def shuffled(l):
    l = copy.deepcopy(l)
    random.shuffle(l)
    return l

UIDs = [f"{i:0>2}" for i in range(100)]

data = [x for x in data if x["id"] in {"onestopqa_0", "onestopqa_6", "onestopqa_11"}]

for uid in UIDs:
    data_out = []

    for line in data[:3]:
        questions = [
            (question, shuffled([{"text": v, "aid": i} for i,v  in enumerate(answers)]))
            for question, answers in line["questions"]
        ]

        mode, text = random.choice(list(line["text"].items()))

        line_out = {
            "id": line["id"],
            "questions": questions,
            "title": line["title"],
            "text": text,
            "mode": mode,
        }
        data_out.append(line_out)

    with open(args.output.replace("UID", uid), "w") as f:
        for line in data_out:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
