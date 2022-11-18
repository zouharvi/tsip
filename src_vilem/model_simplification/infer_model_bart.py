#!/usr/bin/env python3

import argparse
import math
import torch
import tqdm
from transformers import BartTokenizer
from transformers import BartForConditionalGeneration

args = argparse.ArgumentParser()
args.add_argument("--data-test-x", default="data/matchvp_test.complex")
args.add_argument("--model", default="./computed/output/fbasic/checkpoint-final/")
args.add_argument("--output", default="./data/output/bart_fbasic.simple")
args = args.parse_args()


def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data


data_test_txt_x = load_file(args.data_test_x)

tokenizer = BartTokenizer.from_pretrained('facebook/bart-large-cnn')
tokenizer.max_length = 256
data_test_x = tokenizer(data_test_txt_x, truncation=True, padding=True)

model = BartForConditionalGeneration.from_pretrained(args.model).to("cuda")
model.eval()

f_out = open(args.output, "w")

BATCH_SIZE = 32
for b_i in tqdm.tqdm(list(range(math.ceil(len(data_test_x["input_ids"]) / BATCH_SIZE)))):
    input_ids = torch.tensor(
        data_test_x["input_ids"][b_i * BATCH_SIZE:(b_i + 1) * BATCH_SIZE]
    ).to("cuda")
    output_ids = model.generate(input_ids, max_new_tokens=256, num_beams=5).to("cpu")
    output_txt = [tokenizer.decode(line, skip_special_tokens=True) for line in output_ids]
    for line in output_txt:
        f_out.write(line + "\n")
