#!/usr/bin/env python3

import argparse
import spacy

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/matchvp_test.complex")
args.add_argument("-o", "--output", default="data/output/naive_spacy.simple")
args = args.parse_args()

nlp = spacy.load("en_core_web_sm")

def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data

def starts_with_multiple(segment, starts):
    return any([segment.lower().startswith(x) for x in starts])

def contains_multiple(segment, starts):
    return any([x in segment.lower() for x in starts])

def first_word_past(segment):
    result = nlp(segment)[0]
    return result.pos_ == "VERB"

def first_word_number(segment):
    result = nlp(segment)[0]
    return result.pos_ == "NUM"

def split_multiple(line, splitters):
    out = [line]
    for splitter in splitters:
        out_new = []
        for hyp in out:
            out_new += hyp.split(splitter)
        out = out_new
    return out

data_i = load_file(args.input)
data_o = []

SPLITTERS = [" and ", " but ", " when ", " however ", " because ", " though ", " although ", " who ", " that ", " so "]

for line in data_i:
    if contains_multiple(line, SPLITTERS):
        segments = split_multiple(line, SPLITTERS)
        previous_referent = None
        segments_new = []
        for segment in segments:
            if len(segments_new) != 0 and segment[0].isupper():
                # merge to previous one
                segments_new[-1] += " and " + segment
            elif len(segments_new) != 0 and first_word_number(segment):
                # merge to previous one
                segments_new[-1] += " and " + segment
            elif len(segments_new) != 0 and len(segment.split()) <= 3:
                # merge to previous one
                segments_new[-1] += " and " + segment
            elif previous_referent is not None and (starts_with_multiple(segment, ["had", "was", "is", "can", "did", "will"]) or first_word_past(segment)):
                segments_new.append(previous_referent + " " + segment)
            else:
                segments_new.append(segment)

            if contains_multiple(segment, ["she ", " her ", " hers "]):
                previous_referent = "She"
            elif contains_multiple(segment, ["he ", " his ", " him "]):
                previous_referent = "He"
            elif contains_multiple(segment, ["they ", "their ", "theirs "]):
                previous_referent = "They"
            else:
                previous_referent = "It"
        line_local = " . ".join([x[0].upper() + x[1:] for x in segments_new]).rstrip(" ")
        # print(line_local)
        data_o.append(line_local)
    elif " where " in line:
        segments = line.split(" where ")
        segments_new = []
        for segment in segments:
            if len(segments_new) == 0:
                segments_new.append(segment)
            else:
                segments_new.append("There " + segment)
        line_local = " . ".join([x[0].upper() + x[1:] for x in segments_new]).rstrip(" ")
        data_o.append(line_local)
    else:
        print(line)
        data_o.append(line)

with open(args.output, "w") as f:
    f.writelines([x + "\n" for x in data_o])
