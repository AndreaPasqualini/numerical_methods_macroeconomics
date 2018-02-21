import numpy as np
from scipy import linalg as la
from matplotlib import pyplot as plt
#from matplotlib import rc
from time import time
#rc('text', usetex=True)


#%% Solution  =================================================================
""" ---------------------------------------------------------------------------
Some code showcasing how VFI with a stochastic state space works. The main
difficulty is to get the dimensions of the Value Function right. Here, we have
two state variables: capital and Total Factor Productivity (TFP). Hence, the
Value Function will be a matrix: values for capital on the rows, values for
productivity on the columns. Note that N-dimensional arrays are indeed a thing,
both in Python and in Matlab.
--------------------------------------------------------------------------- """

def rouwenhorst(N, mu, rho, sigma):
    def compute_P(p, N):
        if N == 2:
            P = np.array([[p, 1-p],
                          [1-p, p]])
        else:
            Q = compute_P(p, N-1)  # notice recursive function here!
            A = np.zeros((N, N))  # preallocating
            B = np.zeros((N, N))  # preallocating
            A[:N-1, :N-1] += Q  # taking all but last row and last column
            A[1:N, 1:N] += Q  # taking all but first row and first column
            B[:N-1, 1:N] += Q  # taking all but last row and first column
            B[1:N, :N-1] += Q  # taking all but first row and last column
            P = p * A + (1 - p) * B
            P[1:-1, :] /= 2
        return P

    p = (1 + rho) / 2
    P = compute_P(p, N)
    f = np.sqrt(N-1) * (sigma / np.sqrt(1-rho**2))
    s = np.linspace(-f, f, N) + mu
    return s, P


# Parameter and grid initialization  ==========================================
alpha = 0.3
beta = 0.95
delta = 0.1
sigma = 1.5
Nk = 1000
Na = 2

k_ss = ((1 - (1-delta) * beta) / (alpha * beta)) ** (1 / (alpha-1))
k_lo, k_hi = np.array([0.1, 2.5]) * k_ss

K = np.linspace(k_lo, k_hi, num=Nk)

A, P = rouwenhorst(Na, mu=0, rho=0.8, sigma=0.1)
A = np.exp(A)


# Preallocation of matrices  ==================================================
u = np.zeros((Nk, Na))
V0 = np.zeros((Nk, Na))
V1 = np.zeros((Nk, Na))
DRk = np.zeros((Nk, Na), dtype=int)


# VFI  ========================================================================
criterion = 1.
tolerance = 1e-6
n_iter = 0

t0 = time()
while criterion > tolerance:
    n_iter += 1
    for i in range(Nk):
        for j in range(Na):
            C = A[j] * K[i]**alpha + (1 - delta) * K[i] - K
            C[C < 0] = np.nan
            u[:, j] = C ** (1-sigma) / (1-sigma)
        objective = u + beta * V0 @ P.T
        V1[i, :] = np.nanmax(objective, axis=0)
        DRk[i, :] = np.nanargmax(objective, axis=0)
    criterion = np.max(np.max(np.abs(V1 - V0)))
    V0[:] = V1
K1 = K[DRk]
C = np.zeros((Nk, Na))
for j in range(Na):
    C[:, j] = A[j] * K**alpha + (1 - delta) * K - K1[:, j]

t1 = time()
print('Algorithm took {:.3f} seconds with {} iterations'.format((t1-t0),
                                                                n_iter))

k_ss = K1[np.where(np.isclose(K.reshape((-1, 1)), K1))][np.array([2, -3])]


#%% Simulation  ===============================================================
""" ---------------------------------------------------------------------------
Here we get to see one interesting thing we can do: simulation. This is
important because typically with these models one can use Simulated Method of
Moments (SMM) to estimate parameters in a structural fashion. You should take
the course of J. Adda next year if you are interested in seeing what (and how)
you can do with structural models. NOTE: this is not only for Macroeconomists!
You can be any other kind of economist and still need a structural model.
--------------------------------------------------------------------------- """

def ergodic_distribution(pi):
    """
    Given a right-stochastic transition matrix for a Markov Chain, this
    function computes its ergodic distribution using eigenvectors.
    """
    l, v = la.eig(pi)
    vector = v[:, np.where(np.isclose(l, 1.))]
    return (vector / np.sum(vector)).reshape((-1,))


def draw_state(pdf):
    """
    Given a probability distribution function defined over a discrete set, this
    function draws random number distributed with that PDF. The returned value
    is an index.
    """
    cdf = np.cumsum(pdf)
    u = np.random.uniform()
    state_index = np.sum(u - cdf > 0)
    return int(state_index)


def find_nearest(array, value, give_idx=False):
    if array.ndim != 1:
        raise ValueError('Input vector must be uni-dimensional')
    idx = (np.abs(array - value)).argmin()
    if give_idx:
        return idx
    else:
        return array[idx]


T = 250

a = np.zeros((T,), dtype=int)
k = np.zeros((T,), dtype=int)

# Note that I am mainly working with indices here, although I could also use
# interpolation to make everything much more clear (and possibly more precise,
# as long as we stay within the grid we defined at the beginning).
# Also note that the meaningful dynamics here is only described by the policy
# function of capital, given the stochastic state 'a'. I can compute
# consumption, investment, production after the 'for' loop, because those
# values are implied by the series of capital and the series of the shocks.

# Setting initial conditions for the simulations. The stochastic state is
# randomly picked according to the ergodic distribution of the Markov Chain.
# The state of capital is arbitrarily picked from the grid: I pick the
# available point on the grid that is closest to k=3.

a[0] = draw_state(ergodic_distribution(P))    # drawing an index for grid A
k[0] = find_nearest(K, 3, give_idx=True)  # getting index for K
# k[0] = K[0]  # picking the first point on the grid

for t in range(T-1):
    a[t+1] = draw_state(P[a[t], :])  # drawing an index for grid A
    k[t+1] = DRk[k[t], a[t]]         # drawing an index for grid K

capital = K[k]
shocks = A[a]
production = np.zeros((T,))
investment = np.zeros((T,))
consumption = np.zeros((T,))

for t in range(T-1):
    production[t] = shocks[t] * capital[t] ** alpha
    investment[t] = capital[t+1] - (1 - delta) * capital[t]
    consumption[t] = production[t] - investment[t]
production[-1] = shocks[-1] * capital[-1] ** alpha
investment[-1] = np.nan
consumption[-1] = np.nan

y_ss = A * k_ss ** alpha
i_ss = delta * k_ss  # k_ss - (1 - delta) * k_ss
c_ss = y_ss - i_ss


#%% Plotting solutions  =======================================================

colorstate = ['firebrick', 'green']
V_labels = [r'$V(k, a^l)$', r'$V(k, a^h)$']
C_labels = [r'$c(k, a^l)$', r'$c(k, a^h)$']
K_labels = [r"$k'(k, a^l)$", r"$k'(k, a^h)$"]

fig = plt.subplots(figsize=(8, 5))
ax = [None] * 3

pltgrid = (2, 2)
ax[0] = plt.subplot2grid(pltgrid, (0, 0), rowspan=2)
ax[1] = plt.subplot2grid(pltgrid, (0, 1))
ax[2] = plt.subplot2grid(pltgrid, (1, 1))

for a in range(Na):
    ax[0].plot(K, V1[:, a],
               linewidth=2,
               color=colorstate[a],
               label=V_labels[a])
    ax[1].plot(K, K1[:, a],
               linewidth=2,
               color=colorstate[a],
               label=K_labels[a],
               zorder=2)
    ax[2].plot(K, C[:, a],
               linewidth=2,
               color=colorstate[a],
               label=C_labels[a])
ax[1].plot(K, K,
           linewidth=1,
           color='black',
           linestyle='dashed',
           zorder=1)

ax[0].set_title('Value function')
ax[1].set_title('Capital accumulation decision')
ax[2].set_title('Consumption decision')

for a in range(3):
    ax[a].axvline(k_ss[0],
                  color=colorstate[0],
                  linestyle='dotted',
                  zorder=1)
    ax[a].axvline(k_ss[1],
                  color=colorstate[1],
                  linestyle='dotted',
                  zorder=1)
    ax[a].grid(alpha=0.3)
    ax[a].set_xlabel('$k$')
    ax[a].legend()

plt.tight_layout()
fig[0].savefig('./vfi_stochastic.pdf')
plt.show()

#%% Plotting simulations  =====================================================

# Desideratum: background shading when productivity is 'low' (sort of NBER
# recessions). Need to find pairs (a, b) such that 'a' is a date when the
# system goes into recession and 'b' is the earliest successive date when the
# system recovers.

lows = shocks < 1
low_in = [i for i in range(1, T) if (lows[i-1] == False and lows[i] == True)]
low_out = [i for i in range(T-1) if (lows[i] == True and lows[i+1] == False)]
if lows[0] == True:
    low_in.insert(0, 0)
if lows[T-1] == True:
    low_out.append(T-1)

prop_sims = {'color':     'blue',
             'linewidth': 1.5,
             'zorder':    3,
             'label':     'Sample path'}

prop_ss_lo = {'color':     colorstate[0],
              'linewidth': 1,
              'linestyle': 'dashed',
              'zorder':    2,
              'label':     'Low steady state'}

prop_ss_hi = {'color':     colorstate[1],
              'linewidth': 1,
              'linestyle': 'dashed',
              'zorder':    2,
              'label':     'High steady state'}

fig1, ax1 = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True,
                         figsize=(8, 6))

ax1[0, 0].plot(consumption, **prop_sims)
ax1[0, 1].plot(investment,  **prop_sims)
ax1[1, 0].plot(capital,     **prop_sims)
ax1[1, 1].plot(production,  **prop_sims)

ax1[0, 0].axhline(c_ss[0], **prop_ss_lo)
ax1[0, 0].axhline(c_ss[1], **prop_ss_hi)
ax1[0, 1].axhline(i_ss[0], **prop_ss_lo)
ax1[0, 1].axhline(i_ss[1], **prop_ss_hi)
ax1[1, 0].axhline(k_ss[0], **prop_ss_lo)
ax1[1, 0].axhline(k_ss[1], **prop_ss_hi)
ax1[1, 1].axhline(y_ss[0], **prop_ss_lo)
ax1[1, 1].axhline(y_ss[1], **prop_ss_hi)

for i in range(2):
    for j in range(2):
        ax1[i, j].set_xlabel('Time')
        ax1[i, j].grid(alpha=0.3)
        ax1[i, j].legend(framealpha=1)
        for a, b in zip(low_in, low_out):
            ax1[i, j].axvspan(a, b, color='black', alpha=0.1, zorder=1)

ax1[0, 0].set_title('Consumption')
ax1[0, 1].set_title('Investment')
ax1[1, 0].set_title('Capital')
ax1[1, 1].set_title('Production')

plt.tight_layout()
fig1.savefig('./simul_vfi_stochastic.pdf')
plt.show()

