#! /usr/bin/env python3
""""
Run with -h for usage information.
"""
from __future__ import annotations
import argparse
import os
from dataclasses import dataclass, field
from typing import List, Optional
from colorama import init, Fore, Style

# Parse command line arguments
parser = argparse.ArgumentParser(
    description="Compiles all Tier BSP examples one at a time and summarizes the results. Should be run from `atsamd/boards/`.")
parser.add_argument("--warnings", "-w", action="store_true",
                    help="treat warnings as errors")
parser.add_argument("--clippy", "-c", action="store_true",
                    help="run clippy instead of building, treating warnings as errors")
args = parser.parse_args()


@dataclass
class Bsp:
    name: str
    special_examples: List[Example] = field(default_factory=lambda: [])
    features: Optional[List[str]] = None
    flags: Optional[str] = None

    def example_from_filename(self, filename: str) -> Example:
        (name, _) = os.path.splitext(os.path.basename(filename))

        return next(iter([e for e in self.special_examples if e.name == name]), Example(name))

    def examples(self) -> List[Example]:
        return [self.example_from_filename(fname) for fname in sorted(os.listdir(os.path.join(self.name, "examples")))]


@dataclass
class Example:
    name: str
    features: Optional[List[str]] = None

    def slug(self, bsp: Bsp) -> str:
        return os.path.join(bsp.name, self.name)

    def run(self, bsp: Bsp) -> bool:
        wae = "RUSTFLAGS=\"-D warnings\"" if args.warnings or args.clippy else ""
        cmd = "clippy" if args.clippy else "build"
        flags = "" if bsp.flags is None else bsp.flags

        os.chdir(bsp.name)
        res = os.system(
            f"{wae} cargo {cmd} {self.features_flag(bsp)} {flags} --example {self.name}")
        os.chdir("..")
        return res == 0

    def features_flag(self, bsp) -> str:
        if bsp.features is not None:
            return f"--features \"{" ".join(bsp.features)}\""
        elif self.features is not None:
            return f"--features \"{" ".join(self.features)}\""

        return "--all-features"


@dataclass
class Result:
    bsp: Bsp
    example: Example
    success: bool


bsps = [
    Bsp("atsame54_xpro"),
    Bsp("samd11_bare", flags="--release"),
    Bsp("feather_m0", [
        Example("adalogger", ["adalogger", "usb", "sdmmc"]),
        Example("async_dmac", ["dma", "async"]),
        Example("async_eic", ["async"]),
        Example("async_i2c", ["dma", "async"]),
        Example("async_spi", ["dma", "async"]),
        Example("async_uart", ["dma", "async"]),
    ]),
    Bsp("feather_m4"),
    Bsp("metro_m0"),
    Bsp("metro_m4"),
    Bsp("pygamer"),
]

# Compile results
results = []
for bsp in bsps:
    for example in bsp.examples():
        print(f"Compiling {example.slug(bsp)}...")
        results.append(Result(bsp, example, example.run(bsp)))

# Summary
for res in results:
    status_msg = Fore.GREEN + "ok" if res.success else Fore.RED + "FAILED"

    print(f"{res.example.slug(res.bsp)}... {status_msg}" + Style.RESET_ALL)
