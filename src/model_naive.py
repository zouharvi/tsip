#!/usr/bin/env python3

import argparse

args = argparse.ArgumentParser()
args.add_argument("-i", "--input", default="data/matchvp_test.complex")
args.add_argument("-o", "--output", default="data/output/naive.simple")
args = args.parse_args()

def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data

def starts_with_multiple(segment, starts):
    return any([segment.lower().startswith(x) for x in starts])

def contains_multiple(segment, starts):
    return any([x in segment.lower() for x in starts])

def first_word_past(segment):
    first_word = segment.split(" ")[0].lower()
    return first_word.endswith("ed") or first_word.endswith("ook") or first_word.endswith("s")

data_i = load_file(args.input)
data_o = []

for line in data_i:
    if " and " in line:
        segments = line.split(" and ")
        previous_referent = None
        segments_new = []
        for segment in segments:
            if len(segments_new) != 0 and segment[0].isupper():
                # merge to previous one
                segments_new[-1] += " and " + segment
            elif previous_referent is not None and (starts_with_multiple(segment, ["had", "was", "is", "can", "did"]) or first_word_past(segment)):
                segments_new.append(previous_referent + " " + segment)
            else:
                segments_new.append(segment)

            if contains_multiple(segment, ["she ", " her ", " hers "]):
                previous_referent = "She"
            elif contains_multiple(segment, ["he ", " his ", " him "]):
                previous_referent = "He"
            else:
                previous_referent = "It"

        line_local = " . ".join([x[0].upper() + x[1:] for x in segments_new]).rstrip(" ")
        print(line_local)
        data_o.append(line_local)
    else:
        data_o.append(line)

with open(args.output, "w") as f:
    f.writelines([x + "\n" for x in data_o])
