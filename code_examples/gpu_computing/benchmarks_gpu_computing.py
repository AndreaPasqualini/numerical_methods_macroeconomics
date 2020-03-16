# -*- coding: utf-8 -*-
"""
Created on Thu Mar  5 19:16:22 2020

@author: Andrea
"""

from sys import argv
from time import time  # keep track of time
from math import log
from operator import pow as pwr  # exponentiation operator (**)
import numpy as np
import pandas as pd
from numba import jit, cuda, void, float64
from tqdm import trange


#%% Function definitions

# def vmax(V, k_grid, r, y, beta):
#     for ix in range(k_grid.size):
#         VV = pwr(-10.0, 5)
#         for ixp in range(k_grid.size):
#             cons = (1 + r) * k_grid[ix] + y - k_grid[ixp]
#             if cons <= 0:
#                 period_util = pwr(-10, 5)
#             else:
#                 period_util = log(cons)
#             expected = V[ixp]
#             values = period_util + beta * expected
#             if values > VV:
#                 VV = values
#         V[ix] = VV


def vmax(V, k_grid, r, y, beta):
    V_old = np.copy(V)
    for ix in range(k_grid.size):
        cons = (1+r) * k_grid[ix] + y - k_grid
        cons[cons<=0] = np.nan
        period_util = np.log(cons)
        V[ix] = np.nanmax(period_util + beta * V_old)


@jit(void(float64[:], float64[:], float64, float64, float64), nopython=True)
def vmax_jit(V, k_grid, r, y, beta):
    for ix in range(k_grid.size):
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


def time_vfi_cpu(nk, r=0.01, y=1, beta=0.95, tol=1e-4):
    k_grid = np.linspace(0.1, 10, num=nk)
    V_cpu = np.zeros((nk,), dtype=np.float64)
    t0_cpu = time()
    while True:
        V_cpu_old = np.copy(V_cpu)
        vmax(V_cpu, k_grid, r, y, beta)
        crit_cpu = np.max(np.abs(V_cpu - V_cpu_old))
        if crit_cpu < tol:
            break
    t1_cpu = time()
    return t1_cpu - t0_cpu


def time_vfi_jit(nk, r=0.01, y=1, beta=0.95, tol=1e-4):
    k_grid = np.linspace(0.1, 10, num=nk)
    V_jit = np.zeros((nk,), dtype=np.float64)
    t0_jit = time()
    while True:
        V_jit_old = np.copy(V_jit)
        vmax_jit(V_jit, k_grid, r, y, beta)
        crit_jit = np.max(np.abs(V_jit - V_jit_old))
        if crit_jit < tol:
            break
    t1_jit = time()
    return t1_jit - t0_jit


def time_vfi_gpu(nk, r=0.01, y=1, beta=0.95, tol=1e-4):
    cuda_tpb = 1024  # max Threads Per Block (TPB) on RTX 2080Ti
    cuda_threads = nk
    cuda_blocks = cuda_threads // cuda_tpb + 1  # ceil division
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



#%% Main

if __name__ == '__main__':

    out_csv_file = argv[1]
    target = argv[2]  # ['all', 'cpu', 'jit', 'gpu']

    N = 100
    # grid_sizes = range(32, 4352+1, 32)
    grid_sizes = range(5, 1000+1, 5)

    times_cpu = np.zeros((N, len(grid_sizes)))
    times_jit = np.zeros((N, len(grid_sizes)))
    times_gpu = np.zeros((N, len(grid_sizes)))

    if target == 'cpu':
        print('Solving with CPU...')
        for j, nk in enumerate(grid_sizes):
            for i in trange(N, desc='nk = {}'.format(nk)):
                times_cpu[i, j] = time_vfi_cpu(nk)

    elif target == 'jit':
        print('Solving with JIT...')
        for j, nk in enumerate(grid_sizes):
            for i in trange(N, desc='nk = {}'.format(nk)):
                times_jit[i, j] = time_vfi_jit(nk)

    elif target == 'gpu':
        print('Solving with GPU...')
        for j, nk in enumerate(grid_sizes):
            for i in trange(N, desc='nk = {}'.format(nk)):
                times_gpu[i, j] = time_vfi_gpu(nk)

    elif target == 'all':
        for j, nk in enumerate(grid_sizes):
            for i in trange(N, desc='nk = {}'.format(nk)):
                times_cpu[i, j] = time_vfi_cpu(nk)
                times_jit[i, j] = time_vfi_jit(nk)
                times_gpu[i, j] = time_vfi_gpu(nk)

    tmp0_cpu = pd.DataFrame(times_cpu, columns=list(map(str, grid_sizes)))
    tmp0_jit = pd.DataFrame(times_jit, columns=list(map(str, grid_sizes)))
    tmp0_gpu = pd.DataFrame(times_gpu, columns=list(map(str, grid_sizes)))

    tmp1_cpu = tmp0_cpu.melt(var_name='nk', value_name='time')
    tmp1_jit = tmp0_jit.melt(var_name='nk', value_name='time')
    tmp1_gpu = tmp0_gpu.melt(var_name='nk', value_name='time')

    results_cpu = tmp1_cpu.assign(target='cpu')[['target', 'nk', 'time']]
    results_jit = tmp1_jit.assign(target='jit')[['target', 'nk', 'time']]
    results_gpu = tmp1_gpu.assign(target='gpu')[['target', 'nk', 'time']]

    results = pd.concat([results_cpu, results_jit], ignore_index=True)
    results = pd.concat(results_cpu, results_jit, results_gpu,ignore_index=True)

    results.to_csv(out_csv_file)
