"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 7
Proposed solution
==========================================================================  """


import numpy as np


class MarkovChain:


    def __init__(self, pi):
        if not np.allclose(np.sum(pi, axis=1), np.ones(pi.shape[0])):
            raise ValueError('Each row of the input matrix must sum to one.')
        self.Pi = pi

    
    def n_steps_transition(self, n):
        return np.linalg.matrix_power(self.Pi, n)


    def stationary_distribution(self):
        l, v = np.linalg.eig(self.Pi)
        vector = v[:, np.where(np.isclose(l, 1.))]
        return vector / np.sum(vector)


    def simulate(self, T, s):
        """
        It simulates a Markov Chain for T periods given that the initial
        state is 's'. The parameter 's' must be an integer between 0 and
        Pi.shape[0]-1
        """
        if T < 1:
            raise ValueError('The sample length T must be at least 1.')
        if not isinstance(s, int):
            raise TypeError('The initial condition must be an index (integer).')
        if s < 0 or s > self.Pi.shape[0]-1:
            raise ValueError('The initial condition must be a row index of Pi.')

        def draw_state(pdf):
            cdf = np.cumsum(pdf)
            u = np.random.uniform()
            return np.sum(u - cdf > 0)

        sample = np.zeros((T,), dtype=int)
        sample[0] = s
        for t in range(1, T):
            sample[t] = draw_state(self.Pi[sample[t-1], :])

        return sample
