#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
import argparse
import os
from dataclasses import dataclass
from typing import List

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Compiles all Tier BSP examples one at a time and stops if one fails. Should be run from `atsamd/boards/`.")
parser.add_argument("data_dir", metavar="DIR", type=str,
                    help="Lab data directory. Test slugs are assumed to be subdirectories.")
args = parser.parse_args()


@dataclass
class Bsp:
    name: str
    features: List[str]


bsps = [
    Bsp("samd11_bare", ["dma", "async", "rt", "rtic", "use_semihosting"])
]

for bsp in bsps:
