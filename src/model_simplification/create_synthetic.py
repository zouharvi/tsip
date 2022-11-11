#!/usr/bin/env python3

import argparse
import datasets
import tqdm
import random
import re
from itertools import chain

# cat data/synthetic/eli5.complex data/matchvp_train.complex > data/synthetic/eli5_matchvp_train.complex
# cat data/synthetic/eli5.simple data/matchvp_train.simple > data/synthetic/eli5_matchvp_train.simple

args = argparse.ArgumentParser()
args.add_argument("-os", "--output-simple",
                  default="data/synthetic/eli5.simple")
args.add_argument("-oc", "--output-complex",
                  default="data/synthetic/eli5.complex")
args.add_argument("--total", type=int, default=9000)
args = args.parse_args()

data_eli5 = datasets.load_dataset("eli5")
data_a = data_eli5["train_eli5"]
data_b = data_eli5["train_asks"]
data_c = data_eli5["train_askh"]
data = chain(data_a, data_b, data_c)

CONNECTIVES = [
    "and", "and", "and", "and", "and", "and", "and",
    "so", "so",
    "because", "therefore", "but", "then",
    "while", "so that", "when", "however", "though", "although"
]
CONNECTIVES = ["<mask>"]

COLLAPSE_WHITESPACE = re.compile(r'\s+')
random.seed(0)

data_out = []
progress_bar = tqdm.tqdm(data, total=len(data_a) + len(data_b) + len(data_c))
for record in progress_bar:
    if len(data_out) >= args.total:
        break
    for answer in record["answers"]["text"]:
        if any([x in answer for x in ["[", "_", "..", "?", "!"]]):
            continue

        answer = answer.replace("\n", " ")
        answer = answer.replace("*", " ")
        answer = COLLAPSE_WHITESPACE.sub(" ", answer)

        answer_segments = answer.split(". ")
        if len(answer_segments) <= 1:
            continue

        # break if anything is too long or too short
        if any([len(x.split(" ")) >= 10 or len(x) <= 5 for x in answer_segments]):
            continue

        new_simple = answer
        new_complex = ""
        for s_i, segment in enumerate(answer_segments):
            if s_i == 0:
                new_complex += segment
            else:
                connective = random.choice(CONNECTIVES)
                new_complex += " " + connective + " " + \
                    segment[0].lower() + segment[1:] + "."

        new_complex = new_complex.replace("..", ".")
        new_complex = new_complex.replace(". ", " ")
        data_out.append((new_complex, new_simple))
        progress_bar.set_description(f"Collected: {len(data_out)}")

print("Saving", len(data_out))
random.seed(0)
random.shuffle(data_out)

with open(args.output_simple, "w") as f:
    f.writelines([x[1] + "\n" for x in data_out])
with open(args.output_complex, "w") as f:
    f.writelines([x[0] + "\n" for x in data_out])
