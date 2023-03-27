#!/usr/bin/env python3

import argparse
import collections
import load_data
import numpy as np
import scipy.stats as st
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
import fig_utils

_data_flat, data_modes = load_data.load_corpus()


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


data_modes_flat = collections.defaultdict(list)
for mode, data_local in data_modes.items():
    # we need to flatten it because some systems were not evaluated by humans on
    # some texts and those have empty lists in "hihe"
    data_local = [line["mi"] for line in data_local]
    data_modes_flat[mode] += data_local

# sort by SARI
data_modes_flat = dict(sorted(
    data_modes_flat.items(),
    key=lambda x: np.average([
        np.average([v["sari"] for v in x[1]])
    ]),
    reverse=True
))

fig, axs = plt.subplots(3, 3, figsize=(16, 9))

# fix the order
METRICS = list(data_modes_flat["original"][0].keys())
XTICKS = list(range(len(METRICS)))
BARSTYLE = {
    "width": 0.4,
    "linewidth": 1,
    "edgecolor": "black",
}

PRETTYNAMES = {
    "reading_time_est": "read est."
}

for mode_i, (mode, data_local) in enumerate(data_modes_flat.items()):
    ax_fkgl = axs[mode_i // 3][mode_i % 3]
    ax_rest = ax_fkgl.twinx()
    ax_read = ax_fkgl.twinx()

    values = [
        np.average([v[metric] for v in data_local])
        # remove fkgl
        for metric in METRICS[2:]
    ]
    value_fkgl = np.average([v["fkgl"] for v in data_local])
    value_read = np.average([v["reading_time_est"] for v in data_local])

    ax_fkgl.bar(
        [0], -(20-value_fkgl),
        color=fig_utils.COLORS[2],
        bottom=20,
        **BARSTYLE
    )
    ax_read.bar(
        [1], -(60-value_read),
        color=fig_utils.COLORS[1],
        bottom=60,
        **BARSTYLE
    )

    ax_rest.bar(
        XTICKS[2:], values,
        color=fig_utils.COLORS[0],
        **BARSTYLE
    )

    for metric_i, (metric, value) in enumerate(zip(METRICS[2:], values)):
        ax_rest.text(
            x=metric_i+2, y=1.03,
            s=f"{value:.0%}",
            ha="center"
        )

    ax_fkgl.text(
        x=0, y=0.5,
        s=f"{value_fkgl:.1f}",
        ha="center"
    )
    ax_fkgl.text(
        x=1, y=0.5,
        s=f"{value_read:.0f}s",
        ha="center"
    )

    ax_fkgl.set_ylabel(
        r"FKGL $\leftarrow$", color=fig_utils.COLORS[2]
    )
    ax_rest.set_ylabel(
        r"Rest (0-100%) $\rightarrow$",
        color=fig_utils.COLORS[0]
    )

    ax_fkgl.set_ylim(0, 20)
    ax_rest.set_ylim(0, 1.1)
    ax_read.set_ylim(0, 60)
    ax_read.yaxis.set_visible(False)
    ax_fkgl.yaxis.set_visible(False)
    ax_rest.yaxis.set_visible(False)

    ax_fkgl.set_title(f"{mode}")
    ax_fkgl.set_xticks(XTICKS, [
        PRETTYNAMES[x] if x in PRETTYNAMES else x
        for x in METRICS
    ])

plt.suptitle(r"Sorted by SARI")
plt.tight_layout()
plt.show()

exit()
