#!/usr/bin/env python3

import evaluate
import nltk.tokenize
import numpy as np
import easse.fkgl, easse.compression
import tqdm

cache = {}

def evaluate_cache_wrap(metric):
    if metric not in cache:
        cache[metric] = evaluate.load(metric)
    return cache[metric]

def evaluate_empty_wrap(metric):
    if metric in cache:
        del cache[metric]

def eval_bleu(line):
    metric = evaluate_cache_wrap("bleu")
    val = metric.compute(
        predictions=[line["text_system"]],
        references=[[line["text_human_simple"]]])
    return val["bleu"]


def eval_sari(line):
    metric = evaluate_cache_wrap("sari")
    val = metric.compute(
        sources=[line["text_human"]],
        predictions=[line["text_system"]],
        references=[[line["text_human_simple"]]]
    )
    return val["sari"]/100


def eval_bertscore(line):
    metric = evaluate_cache_wrap("bertscore")
    val = metric.compute(
        predictions=[line["text_system"]],
        references=[[line["text_human_simple"]]],
        lang="en"
    )
    return val["f1"][0]

def eval_fkgl(line):
    lines= nltk.tokenize.sent_tokenize(line["text_system"])
    return easse.fkgl.corpus_fkgl(sentences=lines)

def eval_reading_time_estimate(line):
    WPM=200
    WORD_LENGTH=5

    text = line["text_system"]
    text = nltk.tokenize.word_tokenize(text)
    total_bits = sum([len(word)/WORD_LENGTH for word in text])
    return total_bits/WPM*60

def eval_compression(line):
    lines_system= nltk.tokenize.sent_tokenize(line["text_system"])
    lines_ref = nltk.tokenize.sent_tokenize(line["text_human_simple"])
    lines_ref = [[x] for x in lines_ref]
    return easse.compression.corpus_f1_token(
        sys_sents=lines_system,
        refs_sents=lines_ref,
    )/100

def add_all(data):
    for metric_name, metric in [
        ("fkgl", eval_fkgl),
        ("reading_time_est", eval_reading_time_estimate),
        ("compression", eval_compression),
        ("sari", eval_sari),
        ("bleu", eval_bleu),
        ("bertscore", eval_bertscore),
    ]:
        print(metric_name)
        for line in tqdm.tqdm(data):
            metric_val = metric(line)
            line["mi"][metric_name] = metric_val

        # empty memory
        evaluate_empty_wrap(metric_name)