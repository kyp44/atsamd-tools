#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
from __future__ import annotations
import argparse
import os
from dataclasses import dataclass
from typing import List
from colorama import init, Fore, Style

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Compiles all Tier BSP examples one at a time and stops if one fails. Should be run from `atsamd/boards/`.")
parser.add_argument("--warnings", "-w", action="store_true",
                    help="treat warnings as errors")
args = parser.parse_args()


@dataclass
class Bsp:
    name: str
    features: List[str]

    def example_from_filename(self, filename: str) -> Example:
        (name, _) = os.path.splitext(os.path.basename(filename))

        return Example(self, name)

    def examples(self) -> List[Example]:
        return [self.example_from_filename(fname) for fname in sorted(os.listdir(os.path.join(self.name, "examples")))]

    def features_flag(self) -> str:
        return "--all-features"


@dataclass
class Example:
    bsp: Bsp
    name: str

    def slug(self) -> str:
        return os.path.join(self.bsp.name, self.name)

    def clippy(self) -> bool:
        wae = "RUSTFLAGS=\"-D warnings\"" if args.warnings else ""
        os.chdir(self.bsp.name)
        res = os.system(
            f"{wae} cargo clippy {self.bsp.features_flag()} --example {self.name}")
        os.chdir("..")
        return res == 0


@dataclass
class Result:
    example: Example
    success: bool


bsps = [
    Bsp("samd11_bare", []),
    Bsp("feather_m0", []),
    Bsp("metro_m0", []),
    Bsp("feather_m4", []),
    Bsp("metro_m4", []),
    Bsp("pygamer", []),
    Bsp("atsame54_xpro", []),
]

# Compile results
results = []
for bsp in bsps:
    for example in bsp.examples():
        print(f"Compiling {example.slug()}...")
        results.append(Result(example, example.clippy()))

# Summary
for res in results:
    status_msg = Fore.GREEN + "ok" if res.success else Fore.RED + "FAILED"

    print(f"{res.example.slug()}... {status_msg}" + Style.RESET_ALL)
