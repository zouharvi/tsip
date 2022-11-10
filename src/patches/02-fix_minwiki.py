#!/usr/bin/env python3

with open("data/matchvp_test.complex", "r") as f:
    data = [x.rstrip("\n") for x in f.readlines()]
data = [x + ".\n" for x in data if x != "."]
with open("data/matchvp_test.complex", "w") as f:
    f.writelines(data)

with open("data/matchvp_test.simple", "r") as f:
    data = [x.replace(" .", ".") for x in f.readlines()]
with open("data/matchvp_test.simple", "w") as f:
    f.writelines(data)

# with open("data/matchvp_train.complex", "r") as f:
#     data = [x for x in f.readlines()]
# with open("data/matchvp_train.complex", "w") as f:
#     f.writelines(data)

with open("data/matchvp_train.simple", "r") as f:
    data = [x.replace(" ..\n", " .\n").replace(" .", ".") for x in f.readlines()]
with open("data/matchvp_train.simple", "w") as f:
    f.writelines(data)