import cv2
import numpy as np
import math
import os

def cut_image(src_file, annotation_path, des_path, cut_width=100, cut_length=100):
    src_img = cv2.imread(src_file)
    width, length, depth = src_img.shape
    # print("width:{}, length:{}, depth:{}".format(width, length, depth))

    num_width = int(math.ceil(width / cut_width))
    num_length = int(math.ceil(length / cut_length))
    # print("num_width:{}, num_length:{}".format(num_width, num_length))
    img_name = src_file.split('/')[-1].split('.')[0]
    crack_file = "{}/{}_crack.npy".format(annotation_path, img_name)
    repair_file = "{}/{}_repair.npy".format(annotation_path, img_name)
    try:
        crack_label = np.load(crack_file, allow_pickle=True)
    except:
        print(crack_file)
        return
    try:
        repair_label = np.load(repair_file, allow_pickle=True)
    except:
        print(repair_file)
        return
    label_shape = crack_label.shape
    if len(label_shape) < 2:
        print(repair_file)
        return 
    
    dataset = []
    for i in range(num_width):
        for j in range(num_length):
            end_width = min(width, (i + 1) * cut_width)
            end_length = min(length, (j + 1) * cut_length)
            # des_img = np.zeros((cut_width, cut_length, depth))
            des_img = src_img[i * cut_width: end_width, j * cut_length: end_length, :]
            # print("end_width{}".format(end_width))
            des_img = cv2.copyMakeBorder(des_img, 0, max(0, (i + 1 ) * cut_width - end_width),
                            0, max(0, (j + 1) * cut_length - end_length),
                            cv2.BORDER_CONSTANT,
                            value=[255,255,255])
            des_name = "{}/{}_{}_{}.jpg".format(des_path, img_name, i, j)
            cv2.imwrite(des_name, des_img)
            label_1 = crack_label[i][j]
            label_2 = 0 if repair_label[i][j] == 0 else 2
            label = max(0, max(label_1, label_2))
            dataset.append("{} {}".format(des_name, label))
    return dataset


def process_image(base_path, des_path, annotation_path):
    files = os.listdir(base_path)
    dataset = []
    for file_name in files:
        ret = cut_image("{}/{}".format(base_path, file_name), annotation_path, des_path)
        if ret is not None and len(ret) > 0:
            dataset.extend(ret)
    print("sample size : {}".format(len(dataset))) 
    with open(dataset_file, "w") as f:
        for line in dataset:
            f.write("{}\n".format(line))


# input
base_path = "/Users/lvxiao/git/rddc2020/csl_data/road_crack_data/image"
annotation_path = "/Users/lvxiao/git/rddc2020/csl_data/road_crack_data/annotation"

# output
des_path = "/Users/lvxiao/git/road_crack_detect/cut_path"
dataset_file = "/Users/lvxiao/git/road_crack_detect/dataset/all.txt"

process_image(base_path, des_path, annotation_path)
# dataset = cut_image(src_file, annotation_path, des_path)
# print(dataset)

# process_image(base_path, des_path)
