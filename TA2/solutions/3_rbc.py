import numpy as np
from numba import jit, prange
# from matplotlib import rc
from matplotlib import pyplot as plt
from time import time
# rc('text', usetex=True)  # comment out if LaTeX not on your system


#%% Setting up program  =======================================================
beta = 0.99
r = 0.05
phi = 0.5
w = 1

Ns = 500
Nn = 50
S = np.linspace(0.25, 50, num=Ns)
N = np.linspace(0.25, 1, num=Nn)

V0 = np.zeros((Ns,))
V1 = np.zeros((Ns,))
drN = np.zeros((Ns,), dtype=int)
drS = np.zeros((Ns,), dtype=int)


#%% Implementing VFI  =========================================================
"""
Dear future self, this is not working at all. Janky results and unbelievable
saw-like behavior of policy functions. Not pretty. Have a serious look at this
ASAP.
"""
criterion = 1.
tolerance = 1e-6
n_iter = 0

@jit(parallel=True)
def vfi_loop(S, N, V0, w, r):
    Ns = S.size
    Nn = N.size
    for i in prange(Ns):
        C = w * N + (1+r) * S[i] - S.reshape((-1, 1))  # matrix Ns-by-Nn
        C[C<0] = np.nan
        util = np.log(C) - (N**(1+phi)) / (1+phi)  # this is a matrix Ns-by-Nn
        objective = util + beta * np.tile(V0.reshape((-1, 1)), (1, Nn))
        idx_mat = np.nanargmax(objective)
        drS[i], drN[i] = np.unravel_index(idx_mat, dims=objective.shape)
        V1[i] = objective[drS[i], drN[i]]
    return V1, drS, drN

t0 = time()
while criterion > tolerance:
    n_iter += 1
    V1[:], drS[:], drN[:] = vfi_loop(S, N, V0, w, r)
    criterion = np.max(np.abs(V1 - V0))
    V0[:] = V1
    if n_iter % 10 == 0:
        print('Completed {}-th iteration...'.format(n_iter))

t1 = time()
print('VFI took {:.3f} seconds with {} iterations!'.format(t1-t0, n_iter))


S_opt = S[drS]
N_opt = N[drN]
C_opt = w * N_opt + (1+r) * S - S_opt
V_opt = V1


#%% Getting artistic  =========================================================

fig, ax = plt.subplots(figsize=(8, 6))
ax = [None] * 4

pltgrid = (3, 2)

ax[0] = plt.subplot2grid(pltgrid, (0, 0), rowspan=3)  # plotting here VF
ax[1] = plt.subplot2grid(pltgrid, (0, 1))  # plotting here C(S)
ax[2] = plt.subplot2grid(pltgrid, (1, 1))  # plotting here N(S)
ax[3] = plt.subplot2grid(pltgrid, (2, 1))  # plotting here S'(S)

prop_sol = {'linewidth': 2,
            'color': 'red',
            'linestyle': 'solid'}

prop_45 = {'linewidth': 1,
           'color': 'black',
           'linestyle': 'dashed'}

ax[0].plot(S, V_opt, label=r'$V(S)$', **prop_sol)
ax[1].plot(S, C_opt, label=r'$C(S)$', **prop_sol)
ax[2].plot(S, N_opt, label=r'$N(S)$', **prop_sol)
ax[3].plot(S, S_opt, label=r"$S'(S)$", **prop_sol)

ax[3].plot(S, S, label='45 degree line', **prop_45)

for i in range(len(ax)):
    ax[i].legend(framealpha=1)
    ax[i].grid(alpha=0.3)
    ax[i].set_xlabel(r'$S$')

plt.tight_layout()
