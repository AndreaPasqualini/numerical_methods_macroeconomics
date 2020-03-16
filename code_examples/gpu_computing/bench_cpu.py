# -*- coding: utf-8 -*-

from sys import argv
from time import time  # keep track of time
import numpy as np
import pandas as pd
from tqdm import trange


def vmax(V, b_grid, r, y, beta):
    V_old = np.copy(V)
    for ix in range(b_grid.size):
        cons = (1+r) * b_grid[ix] + y - b_grid
        cons[cons<=0] = np.nan
        period_util = np.log(cons)
        V[ix] = np.nanmax(period_util + beta * V_old)


def time_vfi_cpu(nk, r=0.01, y=1, beta=0.95, tol=1e-6):
    b_grid = np.linspace(0.1, 10, num=nk)
    V_cpu = np.zeros((nk,), dtype=np.float64)
    # n_iter = 0
    t0_cpu = time()
    while True:
        # n_iter += 1
        V_cpu_old = np.copy(V_cpu)
        vmax(V_cpu, b_grid, r, y, beta)
        crit_cpu = np.max(np.abs(V_cpu - V_cpu_old))
        # print(crit_cpu)
        if crit_cpu < tol:
            # print('VFI converged in {} iterations.'.format(n_iter))
            break
    t1_cpu = time()
    return t1_cpu - t0_cpu


if __name__ == '__main__':

    N = int(argv[1])
    out_csv_file = argv[2]
    
    # N = 1000
    # out_csv_file = './tmp.csv'

    # grid_sizes = range(32, 4352+1, 32)
    grid_sizes = range(25, 1000+1, 25)

    times_cpu = np.zeros((N, len(grid_sizes)))

    print('Solving with CPU...')
    for j, nk in enumerate(grid_sizes):
        for i in trange(N, desc='nk = {}'.format(nk)):
            times_cpu[i, j] = time_vfi_cpu(nk)

    tmp0_cpu = pd.DataFrame(times_cpu, columns=list(map(str, grid_sizes)))
    tmp1_cpu = tmp0_cpu.melt(var_name='nk', value_name='time')
    results = tmp1_cpu.assign(target='cpu')[['target', 'nk', 'time']]

    results.to_csv(out_csv_file)
