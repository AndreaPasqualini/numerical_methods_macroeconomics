# -*- coding: utf-8 -*-
"""
Filename: class2.py
Bocconi University, Italy

Comparison of Value Function Iteration, Policy Iteration and Projection
methods. See the companion PDF file for a description of this code. The
notation in this file reflects the notation in the PDF file.
"""

# Importing necessary modules =================================================
import numpy as np
from matplotlib import rc  # do not import this if LaTeX is not installed
from matplotlib import pyplot as plt
from time import time


# Defining parameters of the model ============================================
N = 2000
sigma = 1.5
delta = 0.1
beta = 0.95
alpha = 0.3
tolerance = 1e-6

k_ss = ((1 - (1-delta) * beta) / (alpha * beta)) ** (1 / (alpha-1))
k_lo, k_hi = np.array([0.1, 1.9]) * k_ss
K = np.linspace(start=k_lo, stop=k_hi, num=N)


# Preallocation of matrices (for performance) =================================
V_old = np.zeros((N,))
V = np.zeros((N,))
dr = np.zeros((N,), dtype=int)  # this will be a vector of indices


# Value Function Iteration ====================================================
criterion = 1  # dummy value that ensures first execution of 'while'
n_iter = 0
t0 = time()
while criterion > tolerance:
    n_iter += 1  # keeping track of iterations needed for convergence
    for i in range(N):
        C = (K[i] ** alpha) + (1-delta) * K[i] - K
        negative_C = C < 0
        C[negative_C] = np.nan  # enforcing non-negative consumption constraint
        util = (C ** (1-sigma) - 1) / (1-sigma)
        V[i] = np.nanmax(util + beta * V_old)
        dr[i] = np.nanargmax(util + beta * V_old)
    criterion = np.max(np.abs(V - V_old))
    V_old[:] = V
t1 = time()
print('Elapsed time is {:.3f} seconds with {} iterations.'.format(t1-t0,
                                                                  n_iter))

# Computing solutions =========================================================
K_opt = K[dr]
C_opt = K ** alpha + (1-delta) * K - K_opt
# util_opt = (C_opt ** (1-sigma) - 1) / (1-sigma)


# Getting artistic ============================================================
rc('text', usetex=True)  # Comment this out if LaTeX is not installed

fig = plt.subplots(figsize=(8, 5))
ax = [None, None, None]
pltgrid = (2, 4)
ax[0] = plt.subplot2grid(pltgrid, (0, 0), rowspan=2, colspan=2)
ax[1] = plt.subplot2grid(pltgrid, (0, 2), colspan=2)
ax[2] = plt.subplot2grid(pltgrid, (1, 2), colspan=2)

ax[0].plot(K, V,     linewidth=2, color='red',   label=r'$V(k)$')
ax[1].plot(K, K_opt, linewidth=2, color='red',   label=r"$k'(k)$", zorder=2)
ax[2].plot(K, C_opt, linewidth=2, color='red',   label=r'$c(k)$')
ax[1].plot(K, K,     linewidth=1, color='black', linestyle='dashed', zorder=1)
ax[0].set_title('Value function')
ax[1].set_title('Capital accumulation decision')
ax[2].set_title('Consumption decision')

for a in range(3):
    ax[a].axvline(k_ss, linewidth=1, color='black', linestyle='dotted', zorder=1)
    ax[a].grid(alpha=0.3)
    ax[a].set_xlabel('$k$')
    ax[a].legend()

plt.tight_layout()
fig[0].savefig('./vfi_deterministic.pdf')
