# -*- coding: utf-8 -*-
"""
Dummy code that only makes a point about looping over axes in an array. This is
just supposed to show how the so called Curse of Dimensionality affects VFI
methods.
"""

import numpy as np
from time import time

N = 100

X = np.zeros((N, N, N, N))

t0 = time()
for i in range(X.size):
    pass
t1 = time()
print('Loop took {:.3f} seconds'.format(t1-t0))