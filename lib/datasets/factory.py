# --------------------------------------------------------
# Fast R-CNN
# Copyright (c) 2015 Microsoft
# Licensed under The MIT License [see LICENSE for details]
# Written by Ross Girshick
# --------------------------------------------------------

"""Factory method for easily getting imdbs by name."""

__sets = {}

from datasets.aic import aic
from datasets.coco import coco
import numpy as np

for split in ['train', 'val', 'trainval', 'test']:
    name = 'aic_{}'.format(split)
    __sets[name] = (lambda split=split, year=2017: aic(split, 2017))
    __sets[name + "_signal"] = (lambda split=split, year=2017: aic(split, 2017, signal = True))

# Set up coco_2014_<split>
for year in ['2014']:
    for split in ['train', 'val', 'minival', 'valminusminival']:
        name = 'coco_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: coco(split, year))

# Set up coco_2015_<split>
for year in ['2015']:
    for split in ['test', 'test-dev']:
        name = 'coco_{}_{}'.format(year, split)
        __sets[name] = (lambda split=split, year=year: coco(split, year))

def get_imdb(name, signal = False):
    """Get an imdb (image database) by name."""
    if signal != False:
        name = name + "_signal"
    if not __sets.has_key(name):
        raise KeyError('Unknown dataset: {}'.format(name))
    return __sets[name]()

def list_imdbs():
    """List all registered imdbs."""
    return __sets.keys()
