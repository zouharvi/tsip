#!/usr/bin/env python3

import json
import numpy as np
import jezecek.fig_utils
import matplotlib.pyplot as plt
import matplotlib as mpl

with open("computed/paper_example/example_mi.json", "r") as f:
    data1 = json.load(f)
with open("computed/paper_example/example_hi_he_me.json", "r") as f:
    data2 = json.load(f)

data = data1 | data2


def get_nice_name(x):
    x = x.replace("answer correctness", "correctness")
    x = x.replace("answer speed", "speed")
    x = x.replace("time estimation", "time est.")
    x = x.replace("complexity estimation", "complexity est.")
    x = x.replace("simplicity", "simplicity (neg)")
    x = x.capitalize()
    x = x.replace("Bleu", "BLEU")
    x = x.replace("Sari", "SARI")
    return x


# filter constant variables
data = {k: x for k, x in data.items() if np.var(x) != 0}
data_names_pretty = [get_nice_name(x) for x in data.keys()]

data["simplicity"] = [-x for x in data["simplicity"]]

plt.figure(figsize=(7, 3.5))
img = np.full((len(data), len(data)), np.nan)
for m1_i, (metric1, metric1_v) in enumerate(data.items()):
    for m2_i, (metric2, metric2_v) in enumerate(data.items()):
        if m2_i >= m1_i:
            continue
        corr = np.corrcoef(metric1_v, metric2_v)[0, 1]
        img[m1_i, m2_i] = corr
        plt.text(
            m2_i, m1_i - 1, f"{corr:.0%}", ha="center", va="center",
            color="black" if corr < 0.8 else "white"
        )

cmap = mpl.colormaps["YlGn"].copy()

img = np.ma.array(img, mask=np.isnan(img))
cmap.set_bad('white', 1.0)

plt.imshow(
    img[1:, :-1], cmap=cmap, interpolation="nearest",
    aspect="auto"
)
plt.colorbar(pad=0.01)
plt.yticks(
    range(len(data_names_pretty[1:])),
    data_names_pretty[1:]
)
plt.xticks(
    range(len(data_names_pretty[:-1])),
    [("\n\n" if x_i%2 == 0 else "") + x.replace(" ", "\n", 1) for x_i, x in enumerate(data_names_pretty[:-1])],
    rotation=0, ha="center"
)
plt.tight_layout(rect=[0,0,1.04,1], pad=0.2)
plt.savefig("computed/figures/tsip_metric_correlations.pdf")
plt.show()