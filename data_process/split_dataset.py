import os, shutil, random
import numpy as np


dataset_path = '../dataset/custom_dataset'
all_data = '../dataset/all.txt'
val_size, test_size = 0.1, 0.2

all_dataset = []
with open(all_data, 'r') as f:
    for line in f.readlines():
        all_dataset.append(line.strip())

random.shuffle(all_dataset)

train_set = all_dataset[:int(len(all_dataset) * (1 - val_size - test_size))]
val_set = all_dataset[int(len(all_dataset) * (1 - val_size - test_size)):int(len(all_dataset) * (1 - test_size))]
test_set = all_dataset[int(len(all_dataset) * (1 - test_size)):]

os.makedirs(dataset_path, exist_ok=True)
os.makedirs(f'{dataset_path}/train', exist_ok=True)
os.makedirs(f'{dataset_path}/val', exist_ok=True)
os.makedirs(f'{dataset_path}/test', exist_ok=True)

with open(f'{dataset_path}/train/data.txt', "w") as f:
    for line in train_set:
        f.write("{}\n".format(line))

with open(f'{dataset_path}/test/data.txt', "w") as f:
    for line in test_set:
        f.write("{}\n".format(line))

with open(f'{dataset_path}/val/data.txt', "w") as f:
    for line in val_set:
        f.write("{}\n".format(line))