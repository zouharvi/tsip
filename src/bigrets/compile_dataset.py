#!/usr/bin/env python3

import argparse
import collections

args = argparse.ArgumentParser()
args.add_argument("-o", "--output", default="data_bigrets/bigrets.pkl")
args.add_argument("-id", "--input-dir", default="data_bigrets")
args = args.parse_args()


def load_sentence_fusion():
    import csv

    data_out = []

    for splitname, prefix in [
        ("train", "training"),
        ("dev", "development"),
        ("test", "test")
    ]:
        with open(args.input_dir + f"/data/{prefix}.csv", "r") as f:
            data = list(csv.DictReader(f))
        for line in data:
            line_out = {}
            line_out["dataset"] = "Sentence fusion"
            line_out["split"] = splitname
            line_out["simple"] = line["Simplified"]
            line_out["complex"] = line["Original"]
            line_out["source"] = "human" if ("Human" in line["Source"] or "Original" in line["Source"]) else "system"
            line_out["rating"] = {
                "simplicity": float(line["Simplicity"]),
                "adequacy": float(line["Adequacy"]),
            }
            data_out.append(line_out)
        # TODO: it's unclear what "Original" means
        print(line_out)
    return data_out


def load_sscorpus():
    data_out = []

    with open(args.input_dir + f"/sscorpus", "r") as f:
        for line in f:
            line = line.rstrip().split("\t")
            line_out = {}
            line_out["dataset"] = "sscorpus"
            line_out["split"] = "train"
            line_out["simple"] = line[1]
            line_out["complex"] = line[0]
            line_out["source"] = "human"
            data_out.append(line_out)

    return data_out

def load_ewsew_v2():
    data_out = []

    with \
        open(args.input_dir + f"/sentence-aligned.v2/normal.aligned", "r") as f_orig, \
        open(args.input_dir + f"/sentence-aligned.v2/simple.aligned", "r") as f_simple:
        for line_orig, line_simple in zip(f_orig, f_simple):
            line_orig = line_orig.rstrip()
            line_simple = line_simple.rstrip()
            line_out = {}
            line_out["dataset"] = "EW-SEW v2"
            line_out["split"] = "train"
            line_out["simple"] = line_simple
            line_out["complex"] = line_orig
            line_out["source"] = "human"
            data_out.append(line_out)

    return data_out

def load_minwiki():
    data_out = []

    with \
        open(args.input_dir + f"/matchvp_train.complex", "r") as f_orig, \
        open(args.input_dir + f"/matchvp_train.simple", "r") as f_simple:
        for line_orig, line_simple in zip(f_orig, f_simple):
            line_orig = line_orig.rstrip()
            line_simple = line_simple.rstrip()
            line_out = {}
            line_out["dataset"] = "MinWiki"
            line_out["split"] = "train"
            line_out["simple"] = line_simple
            line_out["complex"] = line_orig
            line_out["source"] = "human"
            data_out.append(line_out)

    with \
        open(args.input_dir + f"/matchvp_test.complex", "r") as f_orig, \
        open(args.input_dir + f"/matchvp_test.simple", "r") as f_simple:
        for line_orig, line_simple in zip(f_orig, f_simple):
            line_orig = line_orig.rstrip()
            line_simple = line_simple.rstrip()
            line_out = {}
            line_out["dataset"] = "MinWiki"
            line_out["split"] = "test"
            line_out["simple"] = line_simple
            line_out["complex"] = line_orig
            line_out["source"] = "human"
            data_out.append(line_out)

    return data_out

def load_eli5_synth():
    return []

def load_onestop_qa():
    data_out = []
    import datasets
    data = datasets.load_dataset("onestop_qa")["train"]
    question_buckets = collections.defaultdict(list)
    for line in data:
        question_buckets[(line["title"],line["paragraph_index"])].append(line)
        
    for (title, p_index), lines in question_buckets.items():
        l0_text = [x for x in lines if x["level"] == 0][0]
        l1_text = [x for x in lines if x["level"] == 1][0]
        l2_text = [x for x in lines if x["level"] == 2][0]

        line_out = {}
        line_out["dataset"] = "OnestopQA"
        line_out["split"] = "train"
        line_out["simple"] = l2_text
        line_out["complex"] = l0_text
        line_out["source"] = "human"
        data_out.append(line_out)
    return data_out

data = []
data += load_sentence_fusion()
print(len(data))
data += load_sscorpus()
print(len(data))
data += load_ewsew_v2()
print(len(data))
data += load_minwiki()
print(len(data))
data += load_eli5_synth()
print(len(data))
data += load_onestop_qa()
print(len(data))

print(set([x["source"] for x in data]))