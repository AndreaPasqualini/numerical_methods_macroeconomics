import numpy as np
from scipy import linalg as la


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
        return vector / np.sum(vector)

    def simulate(self, T, s0):
        """
        It simulates a Markov Chain for T periods given that the initial
        state is 's'. The parameter 's0' must be an integer between 0 and
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
