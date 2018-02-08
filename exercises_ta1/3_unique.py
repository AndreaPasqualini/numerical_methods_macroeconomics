"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 3
Proposed solution
==========================================================================  """


def unique(x):
    if not isinstance(x, list):
        raise TypeError('List expected as input.')

    return list(set(x))