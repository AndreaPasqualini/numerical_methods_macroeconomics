# -*- coding: utf-8 -*-

from sys import argv
from time import time  # keep track of time
from math import log
from operator import pow as pwr  # exponentiation operator (**)
import numpy as np
import pandas as pd
from numba import jit, void, float64
from tqdm import trange


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


if __name__ == '__main__':

    N = int(argv[1])
    out_csv_file = argv[2]

    # grid_sizes = range(32, 4352+1, 32)
    grid_sizes = range(25, 1000+1, 25)

    times_jit = np.zeros((N, len(grid_sizes)))

    print('Solving with JIT...')
    for j, nk in enumerate(grid_sizes):
        for i in trange(N, desc='nk = {}'.format(nk)):
            times_jit[i, j] = time_vfi_jit(nk)

    tmp0_jit = pd.DataFrame(times_jit, columns=list(map(str, grid_sizes)))
    tmp1_jit = tmp0_jit.melt(var_name='nk', value_name='time')
    results = tmp1_jit.assign(target='jit')[['target', 'nk', 'time']]

    results.to_csv(out_csv_file)
