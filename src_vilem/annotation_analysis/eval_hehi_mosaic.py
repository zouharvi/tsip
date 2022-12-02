#!/usr/bin/env python3

import argparse
import load_data
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import fig_utils


args = argparse.ArgumentParser()
# args.add_argument()
args = args.parse_args()

data_flat, data_modes = load_data.load_raw()

def mean_yerr(data):
    mean = np.mean(data)
    if len(set(data)) != 1:
        interval = st.t.interval(
            confidence=0.90,
            df=len(data) - 1,
            loc=mean,
            scale=st.sem(data)
        )
        return mean, (interval[1] - interval[0]) / 2
    else:
        return mean, 0

AXIS_COLOR = {
    "acc": fig_utils.COLORS[0],
    "time": fig_utils.COLORS[1],
    "hi": fig_utils.COLORS[2],
}

def plot_yerr_data(axis, axis_name, pos, data):
    mean, yerr = mean_yerr(data)
    axis.errorbar(
        [pos], [mean],
        yerr=yerr,
        capsize=10,
        elinewidth=2,
        capthick=2,
        color=AXIS_COLOR[axis_name],
        fmt="o",
    )


fig, axs = plt.subplots(3,3,figsize=(16,9))
for mode_i, (mode, data_local) in enumerate(data_modes.items()):
    # , gridspec_kw={'height_ratios': [1, 2]}
    # ax = fig.add_subplot(331+mode_i)

    avg_correct = [
        100*np.average([v == 0 for v in line["answers_extrinsic"].values()])
        for line in data_local
    ]
    avg_na = [
        100*np.average([v == -1 for v in line["answers_extrinsic"].values()])
        for line in data_local
    ]
    ax_acc = axs[mode_i%3][mode_i//3]
    ax_time = ax_acc.twinx()
    ax_hi = ax_acc.twinx()

    ax_time.spines["right"].set_position(("data", 5))

    plot_yerr_data(
        axis=ax_acc, axis_name="acc",
        pos=0, data=avg_correct,
    )
    plot_yerr_data(
        axis=ax_acc, axis_name="acc",
        pos=1, data=avg_na,
    )
    for i in [1, 2, 3]:
        times = [line[f"time_{i}"] for line in data_local]
        plot_yerr_data(
            ax_time, axis_name="time",
            pos=i+1, data=times,
        )


    for i in range(5):
        responses = [line["answers_intrinsic"][f"{i}"] for line in data_local]
        plot_yerr_data(
            axis=ax_hi, axis_name="hi",
            pos=7+i, data=responses,
        )

    ax_acc.set_xlim(-1, 12)
    ax_acc.set_ylim(0, 100)
    ax_time.set_ylim(10, 99)
    ax_hi.set_ylim(0, 5)

    # ax_time.
    ax_time.yaxis.set_major_locator(mticker.MultipleLocator(20))


    ax_acc.set_ylabel(r"Accuracy (0 - 100%) $\rightarrow$", color=AXIS_COLOR["acc"])
    ax_time.set_ylabel(r"Time per paragraph (s) $\leftarrow$", color=AXIS_COLOR["time"])
    ax_hi.set_ylabel(r"Rating (0 - 5) $\rightarrow$", color=AXIS_COLOR["hi"])

    ax_acc.set_xticks(
        *zip(*[
            (0, "Acc."),
            (1, "\nN/A."),
            (2, "Read."),
            (3, "\nAnswer."),
            (4, "Interv."),
            (7, "Conf."),
            (8, "\nRecall."),
            (9, "Prec."),
            (10, "\nComplx."),
            (11, "Fluency"),

        ]),
    )

    ax_acc.set_title(f"{mode} ({len(data_local)})")

    # "How confident are you in your answers?",
    # "Did the text provide enough information to answer the questions?",
    # "Did the text contain only necessary information?",
    # "What is the complexity of the text?",
    # "What is the fluency & grammaticality of the text?",

plt.suptitle(r"Spans show 90% confidence intervals. Numbers in brackets show number of samples.")
plt.tight_layout()
plt.show()

exit()