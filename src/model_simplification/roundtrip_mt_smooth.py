#!/usr/bin/env python3

import argparse
import torch
import tqdm

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/synthetic/eli5.complex")
args.add_argument("-o", "--output", default="data/synthetic/eli5_smooth.complex")
args = args.parse_args()

def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data

data_i = load_file(args.input)
fout = open(args.output, "w")

model_ende = torch.hub.load(
    'pytorch/fairseq', 'transformer.wmt19.en-de',
    checkpoint_file='model1.pt:model2.pt',
    tokenizer='moses', bpe='fastbpe'
)
model_deen = torch.hub.load(
    'pytorch/fairseq', 'transformer.wmt19.de-en',
    checkpoint_file='model1.pt:model2.pt',
    tokenizer='moses', bpe='fastbpe'
)

model_ende.eval()
model_ende.to("cuda")
model_deen.eval()
model_deen.to("cuda")

def cycle_translate(batch):
    batch_de = model_ende.translate(batch)
    batch_en = model_deen.translate(batch_de)
    return batch_en

batch = []
for line_i, line_src in enumerate(tqdm.tqdm(data_i)):
    line_src = line_src.rstrip("\n")
    batch.append(line_src)
    if len(batch) == 500:
        batch_out = cycle_translate(batch)
        batch = []
        for line_out in batch_out:
            fout.write(line_out + "\n")
        fout.flush()

if len(batch) != 0:
    batch_out = cycle_translate(batch)
    batch = []
    for line_out in batch_out:
        fout.write(line_out + "\n")
    fout.flush()