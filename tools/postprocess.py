import os
import json
import xml.etree.ElementTree as ET
import argparse
import random
from tqdm import *
parser = argparse.ArgumentParser()
parser.add_argument("in_dir", type = str)
parser.add_argument("out_dir", type = str)
args = parser.parse_args()
OUT = os.path.join(args.in_dir, "AICdevkit")

postfix = ["bicycle", "bus", "car", "groupofpeople", "largetruck", "mediumtruck", "motorcycle", "pedestrian", "smalltruck", "suv", "van", "trafficsignal-green","trafficsignal-yellow","trafficsignal-red"]

ori = os.path.join(OUT, "results/AIC/Main/test_")
if ori[-1] == '/':
    ori = ori[:-1]

path = [ori + x + '.txt' for x in postfix]
data = {}
cnt = 0

'''
Step 1: Read detection
Read all detection bounding boxes into json data
'''

print("Step 1: Read detection")

for p in tqdm(path):
    #print p
    #print postfix[cnt]
    f = open(p, "r")
    for line in f:
        img, conf, xmin, ymin, xmax, ymax = line.split()
        if float(conf) == 0.0:
            continue
        if img not in data:
            data[img] = []
        data[img].append({"class":postfix[cnt], "confidence": float(conf), "xmax": float(xmax), "xmin":float(xmin), "ymax":float(ymax), "ymin":float(ymin)})
    f.close()
    cnt += 1
#f = open("0_output.json", "w")
#json.dump(data, f)
#f.close()

'''
Step 2: Split result and convert name
Split all detection bounding boxes into 3 sub-datasets: 1080p, 720p, 540p(just a downsample version of 1080p result)
Convert classes' names into submission format
'''

print("Step 2: Split result and convert name")
name_table = { "car":"Car",
        "suv":"SUV",
        "smalltruck":"SmallTruck",
        "mediumtruck":"MediumTruck",
        "largetruck":"LargeTruck",
        "pedestrian":"Pedestrian",
        "bus":"Bus",
        "van":"Van",
        "groupofpeople":"GroupOfPeople",
        "bicycle":"Bicycle",
        "motorcycle":"Motorcycle",
        "trafficsignal-green":"Trafficsignal-Green",
        "trafficsignal-yellow":"Trafficsignal-Yellow",
        "trafficsignal-red":"Trafficsignal-Red"
        }
        
data_1080 = {}
data_480 = {}
for k in tqdm(data):
    l = len(data[k])
    for i in xrange(l):
        data[k][i]["class"] = name_table[data[k][i]["class"].lower()]
    if ("hamilton" in k) or ("stevens" in k) or ("walsh" in k):
        data_1080[k] = data[k]
    else:
        data_480[k] = data[k]

f = open(os.path.join(args.out_dir, "1080.json"), "w")
json.dump(data_1080, f, indent = 4, separators = (',', ':'))
f.close()
f = open(os.path.join(args.out_dir, "480.json"), "w")
json.dump(data_480, f, indent = 4, separators = (',', ':'))
f.close()

data_540 = data_1080
for k in tqdm(data_540):
    l = len(data_540[k])
    for i in xrange(l):
        data_540[k][i]["xmax"] = (float(data_540[k][i]["xmax"]) / 2.0)
        data_540[k][i]["xmin"] = (float(data_540[k][i]["xmin"]) / 2.0)
        data_540[k][i]["ymax"] = (float(data_540[k][i]["ymax"]) / 2.0)
        data_540[k][i]["ymin"] = (float(data_540[k][i]["ymin"]) / 2.0)

f = open(os.path.join(args.out_dir, "540.json"), "w")
json.dump(data_540, f, indent = 4, separators = (',', ':'))
f.close()

print("Postprocess Done")
