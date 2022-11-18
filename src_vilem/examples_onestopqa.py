#!/usr/bin/env python3

import datasets
import collections

data = datasets.load_dataset("onestop_qa")["train"]

question_buckets = collections.defaultdict(lambda: collections.defaultdict(list))
for line in data:
    question_buckets[(line["title"],line["paragraph_index"])][line["question"]].append(line)


# print example
example = list(question_buckets.values())[12]
print("\nQUESTIONS")
print(r"\begin{enumerate}[left=-1mm]")
for question_k, question_v in example.items():
    print(r"\item ", question_k)
    print(r"\begin{enumerate}[left=-1mm]")
    for a_i, answer in enumerate(question_v[0]["answers"]):
        # print(f" {chr(ord('a') + a_i)}) {answer}")
        print(r"\item ", answer)
    print(r"\end{enumerate}")
print(r"\end{enumerate}")

print("\nPARAGRAPHS")
# this is a list of paragraphs for the first question but they should be the same
example_paragraphs = list(example.values())[0]
print("Title:", example_paragraphs[0]["title"])

for paragraph in example_paragraphs:
    # print(paragraph.keys(), paragraph["level"])
    print(r"\textbf{Level:} " + str(paragraph["level"]) + r" (human)\\")
    print(r"\textbf{Text:} " + paragraph["paragraph"]  + r"\vspace{2mm}"+ "\n")