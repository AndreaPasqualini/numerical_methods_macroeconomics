"""  ==========================================================================
PhD Eco-Fin, Bocconi University, Milan
Macroeconomics 3
Prof.: Marco Maffezzoli
TA: Andrea Pasqualini

TA session 1 - Exercise 1
Proposed solution
==========================================================================  """


def myMax(x, y):

    if not isinstance(x, (float, int)):
        raise TypeError('Scalar numbers expected as inputs.')

    return max([x,y])
