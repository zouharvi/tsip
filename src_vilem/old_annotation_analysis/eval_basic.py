#!/usr/bin/env python3

import argparse
import load_data
import numpy as np

args = argparse.ArgumentParser()
# args.add_argument()
args = args.parse_args()

data_flat, data_modes = load_data.load_raw()

data = []

for mode, data_local in data_modes.items():
    avg_correct = np.average(
        [[v == 0 for v in line["answers_extrinsic"].values()] for line in data_local])
    avg_intrinsic = [
        np.average([line["answers_intrinsic"][f"{i}"] for line in data_local])
        for i in range(5)
    ]
    avg_intrinsic_text = " ".join([f"{v:.1f}" for v in avg_intrinsic])
    avg_time = np.average([line["time_norm"] for line in data_local])
    print(f"{mode:>30}: [{avg_correct:>3.0%}, {avg_time:>3.0f}s] {avg_intrinsic_text}")

    # "How confident are you in your answers?",
    # "Did the text provide enough information to answer the questions?",
    # "Did the text contain only necessary information?",
    # "What is the complexity of the text?",
    # "What is the fluency & grammaticality of the text?",
