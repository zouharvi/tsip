#!/usr/bin/env python3

import json
import datasets
import collections
import argparse

args = argparse.ArgumentParser()
args.add_argument("-o", "--output", default="computed/onestopqa_extraction.jsonl")
args = args.parse_args()

data = datasets.load_dataset("onestop_qa")["train"]

paragraph_buckets = collections.defaultdict(lambda: collections.defaultdict(list))
for line in data:
    paragraph_buckets[(line["title"],line["paragraph_index"])][line["question"]].append(line)

paragraph_buckets = list(paragraph_buckets.items())

print(len(paragraph_buckets), "unique paragraphs available")

data_out = []

# take first 15
for i, (paragraph_id, example) in enumerate(paragraph_buckets[:15]):
    questions_txt = list(example.keys())
    questions_answer = [
        example[question_txt][0]["answers"]
        for question_txt in questions_txt
    ]
    questions = list(zip(questions_txt, questions_answer))

    title = example[questions_txt[0]][0]["title"]
    text_orig = example[questions_txt[0]][0]["paragraph"]
    text_simple = example[questions_txt[0]][2]["paragraph"]

    line_out = {
        "id": f"onestopqa_{i}",
        "questions": questions,
        "title": title,
        "text": {
            "original": text_orig,
            "human_simple": text_simple,
        }
    }
    data_out.append(line_out)

with open(args.output, "w") as f:
    for line in data_out:
        f.write(json.dumps(line, ensure_ascii=False)+"\n")