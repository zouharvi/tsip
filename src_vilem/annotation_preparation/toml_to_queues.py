#!/usr/bin/env python3

import glob
import toml
import json
import random
import mosestokenizer

random.seed(0)
split_sentence = mosestokenizer.MosesSentenceSplitter(lang="en")

data = [toml.load(f) for f in glob.glob("data_matism/*.toml")]

for i in range(20):
    f = open(f"src_annotation_ui/web/queues/matism/u{i:0>2}.jsonl", "w")
    for text_i, text in enumerate(data):
        lineout = {"id": f"matism_s{i:0>2}"}

        lineout["simplification_type"] = random.choice(list(text["simplification"].keys()))
        lineout["text"] = text["simplification"][lineout["simplification_type"]]["text"]
        lineout["task"] = random.choice(["reading", "ordering"])

        if lineout["task"] == "reading":
            lineout["task_data"] = text["tasks"]["questions"]
        elif lineout["task"] == "ordering":
            sents = list(enumerate(split_sentence([lineout["text"]])))
            random.shuffle(sents)
            lineout["task_data"] = {
                "permutation": [x[0] for x in sents],
                "sentences":  [x[1] for x in sents],
            }
        else:
            raise Exception("Unknown task")

        f.write(json.dumps(lineout, ensure_ascii=False) +"\n")

    f.close()