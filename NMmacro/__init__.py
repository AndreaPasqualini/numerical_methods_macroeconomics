from numpy import sum as summ
from numpy import allclose, isclose, zeros, ones, where, cumsum
from numpy.linalg import matrix_power, eig
from numpy.random import uniform


class MarkovChain:
    def __init__(self, pi):
        if not allclose(summ(pi, axis=1), ones(pi.shape[0])):
            raise ValueError('Each row of the input matrix must sum to one.')
        self.Pi = pi

    def n_steps_transition(self, n):
        return matrix_power(self.Pi, n)

    # @property
    def stationary_distribution(self):
        l, v = eig(self.Pi)
        vector = v[:, where(isclose(l, 1.))]
        return vector / summ(vector)

    def simulate(self, T, s):
        """
        It simulates a Markov Chain for T periods given that the initial
        state is 's'. The parameter 's' must be an integer between 0 and
        Pi.shape[0]-1
        """
        if T < 1:
            raise ValueError('The sample length T must be at least 1.')
        if not isinstance(s, int):
            raise TypeError('Initial condition must be an index (integer).')
        if s < 0 or s > self.Pi.shape[0] - 1:
            raise ValueError('Initial condition must be a row index of Pi.')

        def draw_state(pdf):
            cdf = cumsum(pdf)
            u = uniform()
            return summ(u - cdf > 0)

        sample = zeros((T,), dtype=int)
        sample[0] = s
        for t in range(1, T):
            sample[t] = draw_state(self.Pi[sample[t - 1], :])

        return sample
