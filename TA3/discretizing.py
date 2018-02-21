# -*- coding: utf-8 -*-
"""
Created on Thu Feb 15 16:43:28 2018

@author: Andrea
"""

import numpy as np
from scipy import linalg as la
from scipy.stats import norm
from matplotlib import rc
from matplotlib import pyplot as plt


# Defining the functions for discretizing AR(1) processes  ====================
# Hey, you wanna get the most out of Python? You like being a nerd? Have a look
# at the docstrings, that's how you can use them. Get'em in the "help" window
# in Spyder. Aren't they beautiful? If you're interested, the program (module)
# that parses those docstrings and makes them good-looking is called Sphinx.


def tauchen(N, m, mu, rho, sigma):
    r"""
    Applies Tauchen's method [1]_ to discretize an AR(1) process of the form

    .. math:: x_t = (1-\rho) \mu + \rho x_{t-1} + \varepsilon_t, \qquad
              \varepsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)

    Parameters
    ----------
    N : int
         Number of points on discrete support grid.
    m : float
         Multiplier for setting how far away the endpoints on grid are.
    mu : float
         Unconditional mean of the AR(1) process.
    rho : float
          Persistence parameter in the AR(1) process. Make it within the unit
          circle, please!
    sigma : float
            Standard deviation of the innovation process.

    Returns
    -------
    S : ndarray
         The discrete support grid for the Markov Chain.
    pi : ndarray
         The one-step-ahead transition matrix that matches properties of the
         AR(1) model.

    References
    ----------
    .. [1] Tauchen, G., (1986). "Finite State Markov-Chain Approximations to
           Univariate and Vector Autoregressions." Economics Letters,
           20(2):177–181.
    """
    s_max = m * sigma
    S, step = np.linspace(-s_max, s_max, num=N, retstep=True)
    x = S - rho * S.reshape((-1, 1)) + step / 2
    pi = norm.cdf(x / sigma)
    pi[:, -1] = 1.
    pi[:, 1:] = np.diff(pi)
    S += mu  # centering everything around unconditional mean
    return S, pi


def tauchussey(N, mu, rho, sigma):
    r"""
    Applies Tauchen-Hussey's method [1]_ to discretize an AR(1) process of the
    form

    .. math:: x_t = (1-\rho) \mu + \rho x_{t-1} + \varepsilon_t, \qquad
              \varepsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)

    Parameters
    ----------
    N : int
         Number of points on discrete support grid.
    mu : float
         Unconditional mean of the AR(1) process.
    rho : float
          Persistence parameter in the AR(1) process. Make it within the unit
          circle, please!
    sigma : float
            Standard deviation of the innovation process.

    Returns
    -------
    S : ndarray
         The discrete support grid for the Markov Chain.
    pi : ndarray
         The one-step-ahead transition matrix that matches properties of the
         AR(1) model.

    References
    ----------
    .. [1] G. Tauchen and R. Hussey (1991). "Quadrature-Based Methods for
           Obtaining Approximate Solutions to Nonlinear Asset Pricing Models."
           Econometrica, 59(2):371.
    """
    S, step = np.polynomial.hermite.hermgauss(N)
    S += np.sqrt(2) * sigma
    pdf = (norm.pdf(S, rho * S.reshape((-1, 1)), sigma) /
           norm.pdf(S, 0, sigma))
    pi = step / np.sqrt(np.pi) * pdf
    pi /= pi.sum(axis=1, keepdims=True)
    S += mu  # centering everything around unconditional mean
    return S, pi


def rouwenhorst(N, mu, rho, sigma):
    r"""
    Applies Rouwenhorst's method [1]_ to discretize an AR(1) process of the
    form

    .. math:: x_t = (1-\rho) \mu + \rho x_{t-1} + \varepsilon_t, \qquad
              \varepsilon_t \overset{iid}{\sim} \mathcal{N}(0, \sigma^2)

    Parameters
    ----------
    N : int
         Number of points on discrete support grid.
    mu : float
         Unconditional mean of the AR(1) process.
    rho : float
          Persistence parameter in the AR(1) process. Make it within the unit
          circle, please!
    sigma : float
            Standard deviation of the innovation process.

    Returns
    -------
    S : ndarray
         The discrete support grid for the Markov Chain.
    pi : ndarray
         The one-step-ahead transition matrix that matches properties of the
         AR(1) model.

    References
    ----------
    .. [1] K. A. Kopecky and R. M. H. Suen (2010). "Finite State Markov-Chain
           Approximations to Highly Persistent Processes." Review of Economic
           Dynamics, 13(3):701–714.
    """

    def compute_P(p, N):
        if N == 2:
            P = np.array([[p, 1-p],
                          [1-p, p]])
        else:
            Q = compute_P(p, N-1)
            A = np.zeros((N, N))
            B = np.zeros((N, N))
            A[:N-1, :N-1] += Q
            A[1:N, 1:N] += Q
            B[:N-1, 1:N] += Q
            B[1:N, :N-1] += Q
            P = p * A + (1 - p) * B
            P[1:-1, :] /= 2
        return P

    p = (1 + rho) / 2
    P = compute_P(p, N)
    f = np.sqrt(N-1) * (sigma / np.sqrt(1-rho**2))
    s = np.linspace(-f, f, N) + mu
    return s, P


# Defining few more things  ===================================================
class AR1:

    def __init__(self, alpha, rho, sigma):
        self.alpha = alpha
        self.rho = rho
        self.sigma = sigma
        self.average = alpha / (1 - rho)
        self.stdev = np.sqrt(sigma ** 2 / (1 - rho ** 2))

    def autocov(self, h):
        if h < 0:
            raise ValueError('Specify positive horizon (you know, symmetry...)')
        return self.stdev ** 2 * self.rho ** h

    def simulate(self, T, x0):
        x = np.zeros((T + 2,))
        x[0] = x0
        for t in range(1, T + 2):
            x[t] = (self.alpha + self.rho * x[t - 1] +
                    np.random.normal(scale=self.sigma))

        return x[2:]


class MarkovChain:

    def __init__(self, pi):
        if not np.allclose(np.sum(pi, axis=1), np.ones(pi.shape[0])):
            raise ValueError('Each row of the input matrix must sum to one.')
        self.Pi = pi

    def n_steps_transition(self, n):
        return la.matrix_power(self.Pi, n)

    @property
    def stationary_distribution(self):
        l, v = la.eig(self.Pi)
        vector = v[:, np.where(np.isclose(l, 1.))]
        return (vector / np.sum(vector)).reshape((-1,))

    def simulate(self, T, s0):
        """
        It simulates a Markov Chain for T periods given that the initial
        state is 's'. The parameter 's' must be an integer between 0 and
        Pi.shape[0]-1
        """
        if T < 1:
            raise ValueError('The sample length T must be at least 1.')
        if not isinstance(s0, int):
            raise TypeError('Initial condition must be an index (integer).')
        if s0 < 0 or s0 > self.Pi.shape[0] - 1:
            raise ValueError('Initial condition must be a row index of Pi.')

        def draw_state(pdf):
            cdf = np.cumsum(pdf)
            u = np.random.uniform()
            return np.sum(u - cdf > 0)

        sample = np.zeros((T,), dtype=int)
        sample[0] = s0
        for t in range(1, T):
            sample[t] = draw_state(self.Pi[sample[t - 1], :])

        return sample


""" Finally getting to it  ====================================================
Desiderata: two or three graphs for each method in ('tauchen', 'tauchussey',
'rouwenhorst'). For each method, get graphs in 2-3 rows, 2 columns. Rows are
different because of the assumed 'true' parameters of the AR(1) process,
while in column 0 there will be the actual AR realization and in column 1
there will be the discretized version, simulated using (possibly) the same
initial condition as the AR(1). The graphs need not to be similar in their
path, but must share the same moments: historical average, historical standard
deviation and the extent of persistence. This is not a formal proof for the
adequacy of the methods, but still a useful way to check whether results are
reasonable.
==========================================================================  """

T = 250
mu0 = mu1 = 0.
sigma0 = sigma1 = 1.
rho0, rho1 = 0.25, 0.99

# Applying the various discretization methods
N = 5
m = 3  # only used for Tauchen's method
s_mc0t, p_mc0t = tauchen(N, m, mu0, rho0, sigma0)
s_mc1t, p_mc1t = tauchen(N, m, mu1, rho1, sigma1)
s_mc0th, p_mc0th = tauchussey(N, mu0, rho0, sigma0)
s_mc1th, p_mc1th = tauchussey(N, mu1, rho1, sigma1)

# Simulating two different AR(1) processes: one with low persistence and the
# other with very high persistence. Everything else is the same (i.e.,
# unconditional average and conditional variance). Also simulating the
# corresponding Markov Chains
ar0 = AR1((1 - rho0) * mu0, mu0, sigma0).simulate(T, 0)
ar1 = AR1((1 - rho1) * mu1, mu1, sigma1).simulate(T, 0)
std0 = sigma0 / np.sqrt(1 - rho0 ** 2)
std1 = sigma1 / np.sqrt(1 - rho1 ** 2)

i_mc0t = MarkovChain(p_mc0t).simulate(T, N // 2)  # assuming N odd
i_mc1t = MarkovChain(p_mc1t).simulate(T, N // 2)  # assuming N odd
i_mc0th = MarkovChain(p_mc0th).simulate(T, N // 2)  # assuming N odd
i_mc1th = MarkovChain(p_mc1th).simulate(T, N // 2)  # assuming N odd

mc0t = s_mc0t[i_mc0t]
mc1t = s_mc0t[i_mc1t]
mc0th = s_mc0t[i_mc0th]
mc1th = s_mc0t[i_mc1th]


# Getting artistic  ===========================================================

rc('text', usetex=True)

sets_main = {'linewidth': 1, 'color': 'red'}
sets_avg = {'linewidth': 0.5, 'color': 'black', 'linestyle': 'solid'}
sets_bands = {'linewidth': 0.5, 'color': 'black', 'linestyle': 'dashed'}

figt, axt = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True,
                         figsize=(8, 6))

axt[0, 0].plot(ar0, **sets_main, label='Sample path')
axt[0, 1].plot(mc0t, **sets_main, label='Sample path')
axt[1, 0].plot(ar1, **sets_main, label='Sample path')
axt[1, 1].plot(mc1t, **sets_main, label='Sample path')

for j in range(2):
    axt[0, j].axhline(mu0, **sets_avg, label=r'$\mu_0$')
    axt[0, j].axhline(mu0 - std0, **sets_bands,
                      label=r'$\mu_0 - \sqrt{\sigma_0^2 / (1-\rho_0^2)}$')
    axt[0, j].axhline(mu0 + std0, **sets_bands,
                      label=r'$\mu_1 + \sqrt{\sigma_0^2 / (1-\rho_0^2)}$')

    axt[1, j].axhline(mu1, **sets_avg, label=r'$\mu_1$')
    axt[1, j].axhline(mu1 - std1, **sets_bands,
                      label=r'$\mu_1 - \sqrt{\sigma_1^2 / (1-\rho_1^2)}$')
    axt[1, j].axhline(mu1 + std1, **sets_bands,
                      label=r'$\mu_1 + \sqrt{\sigma_1^2 / (1-\rho_1^2)}$')

for i in range(2):
    for j in range(2):
        axt[i, j].grid(alpha=0.3)
        axt[i, j].set_xlabel('Time')

axt[0, 0].legend(loc='lower left', framealpha=0.85)

axt[0, 0].set_title(r'AR(1) w/$\rho = ' + str(rho0) + '$')
axt[1, 0].set_title(r'AR(1) w/$\rho = ' + str(rho1) + '$')
axt[0, 1].set_title(r'AR(1) passed to Tauchen w/$\rho = ' + str(rho0) + '$')
axt[1, 1].set_title(r'AR(1) passed to Tauchen w/$\rho = ' + str(rho1) + '$')

plt.tight_layout()
# plt.show()
figt.savefig('./tauchen.pdf')


figth, axth = plt.subplots(nrows=2, ncols=2, sharex=True, sharey=True,
                         figsize=(8, 6))

axth[0, 0].plot(ar0, **sets_main, label='Sample path')
axth[0, 1].plot(mc0th, **sets_main, label='Sample path')
axth[1, 0].plot(ar1, **sets_main, label='Sample path')
axth[1, 1].plot(mc1th, **sets_main, label='Sample path')

for j in range(2):
    axth[0, j].axhline(mu0, **sets_avg, label=r'$\mu_0$')
    axth[0, j].axhline(mu0 - std0, **sets_bands,
                      label=r'$\mu_0 - \sqrt{\sigma_0^2 / (1-\rho_0^2)}$')
    axth[0, j].axhline(mu0 + std0, **sets_bands,
                      label=r'$\mu_1 + \sqrt{\sigma_0^2 / (1-\rho_0^2)}$')

    axth[1, j].axhline(mu1, **sets_avg, label=r'$\mu_1$')
    axth[1, j].axhline(mu1 - std1, **sets_bands,
                      label=r'$\mu_1 - \sqrt{\sigma_1^2 / (1-\rho_1^2)}$')
    axth[1, j].axhline(mu1 + std1, **sets_bands,
                      label=r'$\mu_1 + \sqrt{\sigma_1^2 / (1-\rho_1^2)}$')

for i in range(2):
    for j in range(2):
        axth[i, j].grid(alpha=0.3)
        axth[i, j].set_xlabel('Time')

axth[0, 0].legend(loc='lower left', framealpha=0.9)

axth[0, 0].set_title(r'AR(1) w/$\rho = ' + str(rho0) + '$')
axth[1, 0].set_title(r'AR(1) w/$\rho = ' + str(rho1) + '$')
axth[0, 1].set_title(r'AR(1) passed to Tauchen-Hussey w/$\rho = ' + str(rho0) +
                    '$')
axth[1, 1].set_title(r'AR(1) passed to Tauchen-Hussey w/$\rho = ' + str(rho1) +
                    '$')

plt.tight_layout()
# plt.show()
figth.savefig('./tauchen_hussey.pdf')
