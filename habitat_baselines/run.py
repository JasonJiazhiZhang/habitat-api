#!/usr/bin/env python3

# Copyright (c) Facebook, Inc. and its affiliates.
# This source code is licensed under the MIT license found in the
# LICENSE file in the root directory of this source tree.

import argparse
import random

import numpy as np

from habitat_baselines.common.baseline_registry import baseline_registry
from habitat_baselines.config.default import get_config


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--run-type",
        choices=["train", "eval"],
        required=True,
        help="run type of the experiment (train or eval)",
    )
    parser.add_argument(
        "--exp-config",
        type=str,
        required=True,
        help="path to config yaml containing info about experiment",
    )
    parser.add_argument(
        "opts",
        default=None,
        nargs=argparse.REMAINDER,
        help="Modify config options from command line",
    )
    args = parser.parse_args()
    config = get_config(args.exp_config, args.opts)

    random.seed(config.TASK_CONFIG.SEED)
    np.random.seed(config.TASK_CONFIG.SEED)

    trainer_class = baseline_registry.get_trainer(config.TRAINER_NAME)
    assert trainer_class is not None, f"{config.TRAINER_NAME} is not supported"
    trainer = trainer_class(config)

    if args.run_type == "train":
        trainer.train()
    elif args.run_type == "eval":
        trainer.eval()


if __name__ == "__main__":
    main()
