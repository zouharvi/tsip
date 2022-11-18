#!/usr/bin/env python3

import argparse
# import evaluate
import torch
from transformers import BartTokenizer
from transformers import BartForConditionalGeneration, Trainer, TrainingArguments

# metric = evaluate.load("sari")

args = argparse.ArgumentParser()
args.add_argument("--data-train-x", default="data/matchvp_train.complex")
args.add_argument("--data-train-y", default="data/matchvp_train.simple")
args.add_argument("--output", default='computed/output/fbasic/')
args.add_argument("--model", default='facebook/bart-base')
args.add_argument("--epochs", type=int, default=3)
args = args.parse_args()


def load_file(f):
    with open(f, "r") as f:
        data = [x.rstrip() for x in f.readlines()]
    return data


data_train_txt_x = load_file(args.data_train_x)
data_train_txt_y = load_file(args.data_train_y)

tokenizer = BartTokenizer.from_pretrained('facebook/bart-base')
data_train_x = tokenizer(data_train_txt_x, truncation=True, padding=True)
data_train_y = tokenizer(data_train_txt_y, truncation=True, padding=True)
# free up memory
del tokenizer


class DatasetWrapper(torch.utils.data.Dataset):
    def __init__(self, inputs, targets):
        self.inputs = inputs
        self.targets = targets

    def __getitem__(self, index):
        input_ids = torch.tensor(self.inputs["input_ids"][index]).squeeze()
        target_ids = torch.tensor(self.targets["input_ids"][index]).squeeze()
        input_ids.to("cuda")
        target_ids.to("cuda")
        return {"input_ids": input_ids, "labels": target_ids}

    def __len__(self):
        return len(self.targets["input_ids"])


data_train = DatasetWrapper(data_train_x, data_train_y)

training_args = TrainingArguments(
    output_dir=args.output,
    num_train_epochs=args.epochs,
    per_device_train_batch_size=16,
    # per_device_eval_batch_size=1,
    # number of warmup steps for learning rate scheduler
    warmup_steps=200,
    learning_rate=5e-5,
    # strength of weight decay
    weight_decay=0.01,
    logging_dir='./logs',
    logging_steps=100
)

model = BartForConditionalGeneration.from_pretrained(args.model).to("cuda")
model.train()

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=data_train,
    # eval_dataset=data_test,
    # compute_metrics=metric,
)
trainer.train()

model.save_pretrained(args.output + "/checkpoint-final/")
