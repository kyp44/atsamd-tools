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
args = parser.parse_args()


@dataclass
class Bsp:
    name: str
    features: List[str]

    def example_from_filename(self, filename: str):
        (name, _) = os.path.sep(os.path.basename(filename))
        return name


@dataclass
class Example:
    bsp: Bsp
    name: str
    slug: str


bsps = [
    Bsp("samd11_bare", ["dma", "async", "rt", "rtic", "use_semihosting"])
]

for bsp in bsps:
    print(bsp.example_from_filename("test.rs"))
