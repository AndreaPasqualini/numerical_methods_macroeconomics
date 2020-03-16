# -*- coding: utf-8 -*-

from sys import argv
from time import time  # keep track of time
from math import log
from operator import pow as pwr  # exponentiation operator (**)
import numpy as np
import pandas as pd
from numba import cuda, void, float64
from tqdm import trange


@cuda.jit(void(float64[:], float64[:], float64, float64, float64))
def vmax_cuda(V, k_grid, r, y, beta):
    ix = cuda.blockIdx.x * cuda.blockDim.x + cuda.threadIdx.x
    VV = pwr(-10.0, 5)
    for ixp in range(k_grid.size):
        cons = (1 + r) * k_grid[ix] + y - k_grid[ixp]
        if cons <= 0:
            period_util = pwr(-10, 5)
        else:
            period_util = log(cons)
        expected = V[ixp]
        values = period_util + beta * expected
        if values > VV:
            VV = values
    V[ix] = VV


def time_vfi_gpu(nk, r=0.01, y=1, beta=0.95, tol=1e-4):
    cuda_threads = nk
    # cuda_tpb = 640  # Threads Per Block (TPB)
    cuda_blocks = 25
    cuda_tpb = cuda_threads // cuda_blocks
    # cuda_blocks = cuda_threads // cuda_tpb + 1  # ceil division
    block_dims = (cuda_tpb, )    # no. of threads per block
    grid_dims = (cuda_blocks, )  # no. of blocks on grid
    k_grid = np.linspace(0.1, 10, num=nk)
    V_gpu = np.zeros((nk,), dtype=np.float64)
    t0_gpu = time()
    while True:
        V_gpu_old = np.copy(V_gpu)
        vmax_cuda[grid_dims, block_dims](V_gpu, k_grid, r, y, beta)
        cuda.synchronize()  # before proceeding, wait that all cores finish
        crit_gpu = np.max(np.abs(V_gpu - V_gpu_old))
        if crit_gpu < tol:
            break
    t1_gpu = time()
    return t1_gpu - t0_gpu


if __name__ == '__main__':

    N = int(argv[1])
    out_csv_file = argv[2]

    # grid_sizes = range(32, 4352+1, 32)
    grid_sizes = range(25, 1000+1, 25)

    times_gpu = np.zeros((N, len(grid_sizes)))

    print('Solving with GPU...')
    for j, nk in enumerate(grid_sizes):
        for i in trange(N, desc='nk = {}'.format(nk)):
            times_gpu[i, j] = time_vfi_gpu(nk)

    tmp0_gpu = pd.DataFrame(times_gpu, columns=list(map(str, grid_sizes)))
    tmp1_gpu = tmp0_gpu.melt(var_name='nk', value_name='time')
    results = tmp1_gpu.assign(target='gpu')[['target', 'nk', 'time']]

    results.to_csv(out_csv_file)
