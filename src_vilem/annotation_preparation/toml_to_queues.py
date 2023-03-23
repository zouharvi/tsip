#!/usr/bin/env python3

# {"id": "onestopqa_6", "questions": [["When is the new lie detection method expected to work with over 70% accuracy?", [{"text": "It has already achieved this accuracy level in tests", "aid": 0}, {"text": "It is currently not known", "aid": 3}, {"text": "Once it is modified to monitor movements of the entire body", "aid": 2}, {"text": "Within ten years", "aid": 1}]], ["What does the new method of lie detection monitor that the polygraph does not?", [{"text": "Motions in the entire body", "aid": 0}, {"text": "Body temperature", "aid": 3}, {"text": "Body responses to statements about events within a period of ten years", "aid": 2}, {"text": "Talking too much and arm waving", "aid": 1}]], ["When are police stations expected to start using the new lie detection method?", [{"text": "Within 10 years", "aid": 0}, {"text": "It is already in use in many police stations", "aid": 3}, {"text": "Once it is able to track the movements of the entire body", "aid": 2}, {"text": "Once it reaches an accuracy of at least 70%", "aid": 1}]]], "title": "A New Form of Lie Detector Test", "text": "For almost 100 years, police and intelligence agencies around the world have used polygraphs as lie detectors to help convict criminals or unearth spies and traitors. The polygraph is well-liked of the films, with numerous dramatic moments showing the guilty sweating profusely as they are attached. However, the invention may soon be defunct. Researchers in Britain and the Netherlands have made a breakthrough, developing a method that could be in use in police stations around the world within a decade with a success rate of over 70%. Rather than relying on facial tics, talking too much or waving of arms - all seen as tell-tale signs of lying - the new approach involves monitoring full-body movements to detect signs of guilt or deception.", "mode": "muss_syntactic"}


import glob
import toml
import json
import random
import mosestokenizer

random.seed(0)
split_sentence = mosestokenizer.MosesSentenceSplitter(lang="en")

data = [toml.load(f) for f in glob.glob("data_matism/*.toml")]

for i in range(20):
    f = open(f"src_annotation_ui/web/queues/matism/u{i:0>2}.jsonl", "w")
    for text_i, text in enumerate(data):
        lineout = {"id": f"matism_s{i:0>2}"}

        lineout["simplification_type"] = random.choice(list(text["simplification"].keys()))
        lineout["text"] = text["simplification"][lineout["simplification_type"]]["text"]
        lineout["task"] = random.choice(["reading", "ordering"])

        if lineout["task"] == "reading":
            lineout["task_data"] = text["tasks"]["questions"]
        elif lineout["task"] == "ordering":
            sents = list(enumerate(split_sentence([lineout["text"]])))
            random.shuffle(sents)
            lineout["task_data"] = {
                "permutation": [x[0] for x in sents],
                "sentences":  [x[1] for x in sents],
            }
        else:
            raise Exception("Unknown task")

        f.write(json.dumps(lineout, ensure_ascii=False) +"\n")

    f.close()