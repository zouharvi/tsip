#!/usr/bin/env python3

from sklearn.linear_model import LinearRegression
import json
import numpy as np

data_y = [1, 0.9, 0.8, 0.3, 0.7, 0.65]

with open("computed/example.json", "r") as f:
    data_x = [[len(v), np.average([len(w) for w in v.split(" ")])] for x, v in json.load(f).items()]

model = LinearRegression()
model.fit(data_x, data_y)
print("Coef:", model.coef_)
print("Bias:", model.intercept_)