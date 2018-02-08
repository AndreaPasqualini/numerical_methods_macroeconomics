"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 6
Proposed solution
==========================================================================  """


class Fibonacci:

    def __init__(self, n):
        self.n = n

    def element(self):
        if self.n is 0:
            return 0
        elif self.n is 1:
            return 1
        else:
            return self.element() + self.element()

    def series(self):
        return tuple([self.element()] for i in range(self.n))