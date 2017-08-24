#!/bin/bash
set -x
set -e

export PYTHONUNBUFFERED="True"
cd ..

GPU_ID=1
NET="ResNet-101"
DATASET="aic"
SIGNAL=$1

array=( $@ )
len=${#array[@]}
EXTRA_ARGS=${array[@]:3:$len}
EXTRA_ARGS_SLUG=${EXTRA_ARGS// /_}

case $DATASET in
  pascal_voc)
    TRAIN_IMDB="voc_0712_trainval"
    TEST_IMDB="voc_0712_test"
    PT_DIR="pascal_voc"
    ;;
  coco)
    TRAIN_IMDB="coco_2014_train"
    TEST_IMDB="coco_2014_val"
    PT_DIR="coco"
    ITERS=40000
    ;;
  aic)
    TRAIN_IMDB="aic_trainval"
    TEST_IMDB="aic_test"
    PT_DIR="pascal_voc"
    ;;
  *)
    echo "No dataset given"
    exit
    ;;
esac

RPN_MODEL="./output/rfcn_alt_opt_5step_ohem/aic_trainval/stage3_rpn_final.caffemodel"

time ./tools/generate_proposal.py --gpu ${GPU_ID} \
  --net_name ${NET} \
  --weights data/imagenet_models/${NET}-model.caffemodel \
  --imdb ${TRAIN_IMDB} \
  --imdb_test ${TEST_IMDB} \
  --cfg experiments/cfgs/rfcn_alt_opt_5step_ohem.yml \
  --model 'rfcn_alt_opt_5step_ohem' \
  --signal ${SIGNAL} \
  --rpn_model ${RPN_MODEL} \

  ${EXTRA_ARGS}

set +x
set -x

NET_FINAL="./output/rfcn_alt_opt_5step_ohem/aic_trainval/stage2_rfcn_final.caffemodel"

RPN_FINAL="./output/rfcn_alt_opt_5step_ohem/aic_test/stage3_rpn_final_proposals.pkl"
time ./tools/test_net.py --gpu ${GPU_ID} \
  --def models/${PT_DIR}/${NET}/rfcn_alt_opt_5step_ohem/rfcn_test.pt \
  --net ${NET_FINAL} \
  --imdb ${TEST_IMDB} \
  --rpn_file ${RPN_FINAL} \
  --cfg experiments/cfgs/rfcn_alt_opt_5step_ohem.yml \
  --num_dets 400 \
  --signal ${SIGNAL} \
  ${EXTRA_ARGS}
