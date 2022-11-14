#!/usr/bin/env python3

from sklearn.linear_model import LinearRegression
import json

data_y = [24.9, 21.9, 16.4, 9.9, 15.8, 18.7]

with open("computed/example.json", "r") as f:
    data_x = [[len(v)] for x, v in json.load(f).items()]

model = LinearRegression()
model.fit(data_x, data_y)
print("Coef:", model.coef_)
print("Bias:", model.intercept_)