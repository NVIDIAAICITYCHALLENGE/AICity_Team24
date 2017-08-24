# Effective Object Detection From Traffic Camera Videos

## Our [UIUC-IFP](http://ifp-uiuc.github.io) Team:
- Honghui Shi
- Zhichao Liu
- Yuchen Fan
- Xinchao Wang
- Prof. Thomas Huang

## Our Implementation for Nvidia AI City Challenge

Our implementation **py-rfcn** is adapted from py-R-FCN, with additions and modification to support our winning solution to the 1st [IEEE Smart World Nvidia AI City Challenge](http://smart-city-conference.com/AICityChallenge/index.html).
(For usage and installation of the original py-R-FCN, please refer to [here](README_old.md).)

## code usage 

### 1. Prepare dataset
(your code is in `py-rfcn`)
```
$ cd py-rfcn
$ cd tools
$ python ./preprocess.py .. your_tmp_path
```
### 2. Build from source 
(your aic dataset is in `/dataset`)
```
$ sh compile.sh your_tmp_path /dataset
```

### 3. Test on our pre-trained model
Download models from [here][1].

Put `ResNet-101-model.caffemodel` in `py-rfcn/data/imagenet_models/`

Put `aic_trainval` in `py-rfcn/output/rfcn_alt_opt_5step_ohem`
```
$ bash test.sh 0
```

### 4. Train on aic dataset
We find it is better to train vehicle detector separately from traffic-signal detector.

if you want to train without traffic-signal
```
$ sh train.sh 0
```
if you want to train on traffic-signal
```
$ sh train.sh 1
```
### 5. Postprocess for submission
```
$ python postprocess.py your_tmp_dir output_dir
```
[1]: https://www.dropbox.com/sh/5aoifg78vsnhivp/AAC1gwf07beBoVapLpFTNdN6a?dl=0

## Acknowledgement
This work is supported in part by IBM-ILLINOIS Center for Cognitive Computing Systems Research (C3SR) - a research collaboration as part of the IBM Cognitive Horizons Network.

