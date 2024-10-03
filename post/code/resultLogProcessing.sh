#!/bin/bash
awk '{gsub(/std::vector of length/, "\nstd::vector of length"); print}' results.log > result_lines.log

