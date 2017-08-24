import os
import xml.etree.ElementTree as ET
import argparse
import random
from tqdm import *

parser = argparse.ArgumentParser()
parser.add_argument("in_dir", type = str)
parser.add_argument("out_dir", type = str)
args = parser.parse_args()
OUT = os.path.join(args.out_dir, "AICdevkit")
if not os.path.exists(OUT):
    os.mkdir(OUT)
out_aic = os.path.join(OUT, "AIC")
if not os.path.exists(out_aic):
    os.mkdir(out_aic)
dir_list = [out_aic]
for d in dir_list:
    os.mkdir(os.path.join(d, "Annotations"))
    os.mkdir(os.path.join(d, "ImageSets"))
    os.mkdir(os.path.join(d, "ImageSets", "Main"))
    os.mkdir(os.path.join(d, "JPEGImages"))
    os.mkdir(os.path.join(d, "LightAnnotations"))

'''
Step 1: Clean data
clip bounding boxes to the bound of the image and delete useless annotations
'''

print("Step 1: Clean Data")

args = parser.parse_args()
ANN_DIR = [os.path.join(args.in_dir, "aic1080-voc/Annotations/"), os.path.join(args.in_dir, "aic480-voc/Annotations/")]

for ann_dir in ANN_DIR:
    anns = os.listdir(ann_dir)
    for ann in tqdm(anns):
        path = os.path.join(ann_dir, ann)
        tree = ET.parse(path)
        objs = tree.findall('object')
        size = tree.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        #print "Width ", width
        #print "Height ", height
        father = tree.getroot()
        for i, obj in enumerate(objs):
            cls = obj.find('name').text.lower().strip()
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            x1 = float(bbox.find('xmin').text) - 1
            y1 = float(bbox.find('ymin').text) - 1
            x2 = float(bbox.find('xmax').text) - 1
            y2 = float(bbox.find('ymax').text) - 1
            if(x1>x2 or y1 > y2 or "traffic" in cls):
                father.remove(obj)
            elif x1 < 0 or x2 >= width or y1 < 0 or y2 >= height:
                x1 = max(x1, 0)
                bbox.find('xmin').text = str(x1 + 1.)
                y1 = max(y1, 0)
                bbox.find('ymin').text = str(y1 + 1.)
                x2 = min(x2, width - 1)
                bbox.find('xmax').text = str(x2 + 1.)
                y1 = min(y2, height - 1)
                bbox.find('ymax').text = str(y2 + 1.)
        tree.write(os.path.join(out_aic, "Annotations", ann), encoding = "utf-8", xml_declaration = True)

'''
Step 2: Split dataset for traffic-signal
'''
print("Step 2: Split dataset for traffic-signal")

for ann_dir in ANN_DIR:
    anns = os.listdir(ann_dir)
    for ann in tqdm(anns):
        path = os.path.join(ann_dir, ann)
        tree = ET.parse(path)
        objs = tree.findall('object')
        size = tree.find('size')
        width = int(size.find('width').text)
        height = int(size.find('height').text)
        #print "Width ", width
        #print "Height ", height
        father = tree.getroot()
        for i, obj in enumerate(objs):
            cls = obj.find('name').text.lower().strip()
            bbox = obj.find('bndbox')
            # Make pixel indexes 0-based
            x1 = float(bbox.find('xmin').text) - 1
            y1 = float(bbox.find('ymin').text) - 1
            x2 = float(bbox.find('xmax').text) - 1
            y2 = float(bbox.find('ymax').text) - 1
            if(x1>x2 or y1 > y2 or "traffic" not in cls):
                father.remove(obj)
            elif x1 < 0 or x2 >= width or y1 < 0 or y2 >= height:
                x1 = max(x1, 0)
                bbox.find('xmin').text = str(x1 + 1.)
                y1 = max(y1, 0)
                bbox.find('ymin').text = str(y1 + 1.)
                x2 = min(x2, width - 1)
                bbox.find('xmax').text = str(x2 + 1.)
                y1 = min(y2, height - 1)
                bbox.find('ymax').text = str(y2 + 1.)
        tree.write(os.path.join(out_aic, "LightAnnotations", ann), encoding = "utf-8", xml_declaration = True)



'''
Step 3: Split dataset into train and val datasets
Resplit dataset into train set and validation set (10 : 1)
'''

print("Step 3: Split dataset into train and val datasets")

TXT_DIR = [os.path.join(args.in_dir, "aic1080-voc/ImageSets/Main"), os.path.join(args.in_dir, "aic480-voc/ImageSets/Main")]
TAR_DIR = os.path.join(out_aic, "ImageSets", "Main")
l = []
for txt_dir in TXT_DIR:
    ori_train = os.path.join(txt_dir, "train.txt")
    ori_val = os.path.join(txt_dir, "val.txt")

    f_t = open(ori_train, "r")
    f_v = open(ori_val, "r")

    for i in f_t:
        l.append(i)
    for i in f_v:
        l.append(i)
    f_t.close()
    f_v.close()

random.shuffle(l)
length = len(l)
train_len = int(length * 10.0 / 11)
train_l = l[:train_len]
val_l = l[train_len:]
tar_train = os.path.join(TAR_DIR, "trainval.txt")
tar_val = os.path.join(TAR_DIR, "test.txt")
f_t = open(tar_train, "w")
f_v = open(tar_val, "w")
f_t.writelines(train_l)
f_v.writelines(val_l)
f_t.close()
f_v.close()

outs = [tar_train, tar_val]
for out in outs:
    name = out[:-4] + "_signal.txt"
    output = open(name, "w")
    cin = open(out, "r")
    for line in tqdm(cin):
        path = os.path.join(os.path.join(out_aic, "LightAnnotations"), line.strip() + '.txt')
        tree = ET.parse(path)
        objs = tree.findall('object')
        if len(objs) <= 0:
            continue
        else:
            output.write(line)
    cin.close()
    output.close()

print("Preprocess done")
