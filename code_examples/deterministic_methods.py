# -*- coding: utf-8 -*-
"""
title: Deterministic Methods
author: Andrea Pasqualini
created: 20 January 2019

This script showcases the use of the class NMmacro.models.NCGM that I wrote.
"""

#%% Importing necessary packages and setting up working directory

import sys
sys.path.insert('../')

import numpy as np
from NMmacro.models import NCGM


#%% Calibrating and solving the model

alpha = 0.3
beta = 0.95
gamma = 1.5
delta = 0.1

k_ss = ((1 - (1-delta) * beta) / (alpha * beta)) ** (1 / (alpha-1))
k_lo, k_hi = np.array([0.1, 1.9]) * k_ss

k = np.linspace(start=k_lo, stop=k_hi, num=1000)

# initial condition for PFI
guess_c_pfi = 0.1 * np.ones(k.shape)

# initial condition for direct projection
guess_c_proj = 0.4 + 0.35 * k - 0.02 * k**2

mdl = NCGM(alpha, beta, gamma, delta)
vfi_cp, vfi_kp, vfi_v = mdl.solve_vfi(k)
pfi_cp, pfi_kp = mdl.solve_pfi(k, guess_c_pfi)
pro_cp, pro_kp = mdl.solve_proj(k, guess_c_proj)


#%% Plotting results

mdl.plot_solution(k, vfi_cp, vfi_kp, vfi_v)
mdl.plot_solution(k, pfi_cp, pfi_kp)
mdl.plot_solution(k, pro_cp, pro_kp)
