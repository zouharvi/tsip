#!/usr/bin/env python3

import collections
import json
import evaluate
import numpy as np

with open("computed/example.json", "r") as f:
    data = json.load(f)


cache = {}

def evaluate_cache_wrap(metric):
    if metric not in cache:
        cache[metric] = evaluate.load(metric)
    return cache[metric]

def evaluate_empty_wrap(metric):
    del cache[metric]

def eval_bleu(hyp, data):
    metric = evaluate_cache_wrap("bleu")
    val = metric.compute(predictions=[hyp], references=[[data["human_2"]]])
    return val["bleu"]*100


def eval_sari(hyp, data):
    metric = evaluate_cache_wrap("sari")
    val = metric.compute(
        sources=[data["human_0"]],
        predictions=[hyp],
        references=[[data["human_2"]]]
    )
    return val["sari"]


def eval_bertscore(hyp, data):
    metric = evaluate_cache_wrap("bertscore")
    val = metric.compute(
        predictions=[hyp],
        references=[[data["human_2"]]],
        lang="en"
    )
    return val["f1"][0]


def eval_reading_time_estimation(hyp, data):
    return len(hyp)*0.026 + 0.456

def eval_complexity_estimation(hyp, data):
    chars = len(hyp)
    word_length = np.average([len(w) for w in hyp.split(" ")])
    return chars*0.002 + word_length*0.175 -1.213

results = collections.defaultdict(list)
for metric_name, metric in [
    ("sari", eval_sari),
    ("bleu", eval_bleu),
    ("bertscore", eval_bertscore),
    ("complexity estimation", eval_complexity_estimation),
    ("reading time estimation", eval_reading_time_estimation),
]:
    print(metric_name)
    for model_name, model_text in data.items():
        metric_val = metric(model_text, data)
        print(f"{model_name:>20}: {metric_val:.2f}")
        results[metric_name].append(metric_val)

with open("computed/example_mi.json", "w") as f:
    json.dump(results, f)
