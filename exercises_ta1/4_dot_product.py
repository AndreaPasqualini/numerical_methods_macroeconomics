"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 4
Proposed solution
==========================================================================  """


def times(a, b):
    
    if not isinstance(a, list) or not isinstance(b, list):
        raise TypeError('Lists expected as inputs.')
    
    if not len(a) == len(b):
        raise ValueError('Lists of equal length expected as inputs')
    
    if len(a) == 0:
        return None

    return sum(i * j for i, j in zip(a, b))