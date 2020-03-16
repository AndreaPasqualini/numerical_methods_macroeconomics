#!/bin/bash

python ./bench_jit.py 1000 ./results_jit.csv
python ./bench_cpu.py 1000 ./results_cpu.csv
python ./bench_gpu.py 1000 ./results_gpu.csv
