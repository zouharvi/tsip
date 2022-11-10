#!/usr/bin/env python3

import argparse
import tqdm
from transformers import pipeline
import re

# cat data/synthetic/eli5_masked_un.complex data/matchvp_train.complex > data/synthetic/eli5_masked_matchvp_train.complex
# cat data/synthetic/eli5_masked.simple data/matchvp_train.simple > data/synthetic/eli5_masked_matchvp_train.simple

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/synthetic/eli5_masked.complex")
args.add_argument("-o", "--output", default="data/synthetic/eli5_masked_un.complex")
args = args.parse_args()

COLLAPSE_WHITESPACE = re.compile(r'\s+')

def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data

data_i = load_file(args.input)
fout = open(args.output, "w")

model_unmasker = pipeline('fill-mask', model='roberta-base', device=0)

def unmask_sentence(sent):
    while "<mask>" in sent:
        sent = sent.replace("<mask>", " <mask> ")
        sent = COLLAPSE_WHITESPACE.sub(" ", sent)
        out = model_unmasker(sent)
        # always wrap it
        if type(out[0]) != list:
            out = [out]
        sent = out[0][0]["sequence"].replace("<s>", "").replace("</s>", "")
    return sent



for line in tqdm.tqdm(data_i):
    line_smooth = unmask_sentence(line)
    fout.write(line_smooth + "\n")