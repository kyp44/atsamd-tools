#!/bin/bash

# Exit on error
set -e

procs=("samd11c" "samd11d" "samd21e" "samd21g" "samd21j" "samd21el" "samd21gl" "samd51g" "samd51j" "samd51n" "samd51p" "same51g" "same51j" "same51n" "same53j" "same53n" "same54n" "same54p")

for proc in "${procs[@]}"; do
    cargo check --features "$proc rtic"
done
