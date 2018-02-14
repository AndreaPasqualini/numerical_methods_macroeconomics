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
from matplotlib import rc
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

C0 = 0.1 * np.ones((N,), dtype=int)

criterion = 1.
tolerance = 1e-6
n_iter = 0


# Policy Function Iteration  ==================================================
t0 = time()

while criterion > tolerance:
    n_iter += 1
    K_opt = (K ** alpha - C0) + (1 - delta) * K
    pc = np.polyfit(K, C0, 5)
    Ctp1 = np.polyval(pc, K_opt)
    opr = alpha * K_opt ** (alpha-1) + 1 - delta
    C1 = Ctp1 * (beta * opr) ** (-1 / sigma)
    criterion = np.max(np.abs(C1 - C0))
    C0[:] = C1

t1 = time()
print('Elapsed time is {:.3f} seconds with {} iterations.'.format(t1-t0,
                                                                  n_iter))


# Getting artistic ============================================================
rc('text', usetex=True)

fig, ax = plt.subplots(nrows=1, ncols=2, figsize=(8, 5))

ax[0].plot(K, K_opt, color='red', linewidth=2, zorder=2, label=r"$k'(k)$")
ax[1].plot(K, C1, color='red', linewidth=2, zorder=2, label=r'$c(k)$')
ax[0].plot(K, K, color='black', linewidth=1, linestyle='dashed', zorder=1)

ax[0].set_title('Capital accumulation decision')
ax[1].set_title('Consumption decision')

for a in range(2):
    ax[a].axvline(k_ss, color='black', linewidth=1, linestyle='dotted', zorder=1)
    ax[a].legend()
    ax[a].grid(alpha=0.3)
    ax[a].set_xlabel(r'$k$')

plt.tight_layout()
fig.savefig('./pfi_deterministic.pdf')
