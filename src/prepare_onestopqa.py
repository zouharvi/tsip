
import datasets
import collections
import random

data = datasets.load_dataset("onestop_qa")["train"]

question_buckets = collections.defaultdict(lambda: collections.defaultdict(list))
for line in data:
    question_buckets[(line["title"],line["paragraph_index"])][line["question"]].append(line)