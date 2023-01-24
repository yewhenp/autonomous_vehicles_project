#!/usr/bin/env python3
"""
Scripts to train a keras model using tensorflow.
Basic usage should feel familiar: train.py --tubs data/ --model models/mypilot.h5

Usage:
    train.py [--tubs=tubs] (--model=<model>)
    [--type=(linear|inferred|tensorrt_linear|tflite_linear)] [--train-stage=(0|1|2)] [--load-weights=(true|false)]
    [--comment=<comment>]

Options:
    -h --help              Show this screen.
"""

from docopt import docopt


import donkeycar as dk
from donkeycar.pipeline.training import train


def main():
    args = docopt(__doc__)
    cfg = dk.load_config()
    tubs = args['--tubs']
    model = args['--model']
    model_type = args['--type']
    comment = args['--comment']
    train_stage = int(args['--train-stage'])
    load_weights = args['--load-weights'] == "true"
    train(cfg, tubs, model, model_type, comment, train_stage=train_stage, load_weights=load_weights)


if __name__ == "__main__":
    main()
