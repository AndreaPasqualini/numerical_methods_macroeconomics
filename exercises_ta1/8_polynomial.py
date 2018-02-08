"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 8
Proposed solution
==========================================================================  """


from numpy import linspace
from matplotlib.pyplot import subplots


class Poly:

    def __init__(self, a):
        if not isinstance(a, tuple):
            raise TypeError('Tuple expected as input.')
        self.a = a


    def evaluate(self, x0):
        return sum(ai * x0**i for i, ai in enumerate(self.a))


    def differentiate(self, x0):
        b = [i * ai for i, ai in enumerate(self.a)]
        b = b[1:]
        return sum(bi * x0**i for i, bi in enumerate(b))


    def plot(self, x_min, x_max):
        domain = linspace(x_min, x_max, 1000)
        image = [self.evaluate(x) for x in domain]
        fig, ax = subplots(figsize=[8,6])
        ax.plot(domain, image, color='black', linewidth=2)
        ax.grid(alpha=0.3)
        # fig.savefig('./polyplot.pdf')

