#!/usr/bin/env python3

import evaluate
import argparse

args = argparse.ArgumentParser()
args.add_argument("-s", "--source", default="data/matchvp_test.complex")
args.add_argument("-p", "--prediction", default="data/matchvp_test.complex")
args.add_argument("-r", "--reference", default="data/matchvp_test.simple")
args = args.parse_args()

def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data

metric = evaluate.load("sari")

data_s = load_file(args.source)
data_p = load_file(args.prediction)
data_r = load_file(args.reference)
data_r = [[x] for x in data_r]

score = metric.compute(sources=data_s, predictions=data_p, references=data_r)
print(f"SARI score: {score['sari']:.1f}%")