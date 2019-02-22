from time import time
import numpy as np
from scipy import optimize as opt
from matplotlib import pyplot as plt


class NCGM:
    """
    This is the (deterministic) NeoClassical Growth Model (NCGM). The model
    is instantiated with a set of calibrated parameters. The 'solve' methods
    (VFI, PFI and TI) will take the grid for the state variable(s) as input
    arguments.
    """

    def __init__(self, alpha=0.3, beta=0.95, gamma=1.5, delta=0.1):
        """
        PARAMETERS
        ----------
        alpha : float (default is 0.3)
                The exponent in the production function, a.k.a. the intensity
                of capital in production.
        beta : float (default is 0.95)
               The discount rate of the agent.
        gamma : float (default is 1.5)
                The coefficient of relative risk aversion of the agent.
        delta : float (default is 0.1)
                The depreciation rate of capital.
        """
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        self.delta = delta
        self.u = lambda c: (c**(1-self.gamma)) / (1-self.gamma)
        self.k_ss = ((1 - (1-delta) * beta) / (alpha * beta))**(1 / (alpha-1))


    def _euler(self, c0, k):
        """
        Implements the Euler Equation given a guess for the consumption level
        c_t and for various levels of capital holdings k_t. It returns the
        quantity resid = LHS - RHS.
        """
        k1 = k**self.alpha - c0 + (1-self.delta) * k
        pc = np.polyfit(k, c0, 1)
        ctp1 = np.polyval(pc, k1)
        opr = self.alpha * k1 ** (self.alpha-1) + 1 - self.delta
        resid = c0 - ctp1 * (self.beta * opr) ** (-1/self.gamma)
        return resid


    def solve_vfi(self, k, tolerance=1e-6):
        """
        This method takes a grid for the state variable and solves the Bellman
        problem by Value Function Iteration. It returns the policy functions
        and the computed value at the optimum. It also prints to display how
        much time and how many iterations were necessary to converge to the
        solution.

        PARAMETERS
        ----------
        k : numpy.array
             The grid for the state variable over which the Value Function is
             computed. The resulting policy functions will be computed at the
             gridpoints in this array.
        tolerance : float (optional, default is 10**(-6))
                    The value against which the sup-norm is compared to when
                    determining whether the algorithm converged or not.

        RETURNS
        -------
        c_opt : numpy.array
                The policy function for consumption, evaluated at the
                gridpoints 'k'.
        k_opt : numpy.array
                The policy function for capital holdings, evaluated at the
                gridpoints 'k'.
        v_opt : numpy.array
                The value function computed at the gridpoints 'k'.
        """

        n = k.shape[0]

        v_old = np.zeros((n,))
        v = np.zeros((n,))
        dr = np.zeros((n,), dtype=int)

        criterion = 1
        n_iter = 0

        t0 = time()

        while criterion > tolerance:
            n_iter += 1
            for i in range(n):
                C = (k[i] ** self.alpha) + (1 - self.delta) * k[i] - k
                negative_C = C < 0
                C[negative_C] = np.nan
                objective = self.u(C) + self.beta * v_old
                v[i] = np.nanmax(objective)
                dr[i] = np.nanargmax(objective)
            criterion = np.max(np.abs(v - v_old))
            v_old[:] = v  # forcing a deep copy of the array

        t1 = time()

        k_opt = k[dr]
        c_opt = k ** self.alpha + (1-self.delta) * k - k_opt

        print('VFI took {} iterations and {:.3f} seconds to converge'.format(n_iter, t1 - t0))
        return (c_opt, k_opt, v)


    def solve_pfi(self, k, c0, tolerance=1e-6):
        """
        This method takes a grid for the state variable and solves the Bellman
        problem by Policy Function Iteration. As the convergence of PFI depends
        on the initial condition, a guess must be provided by the user. The
        method returns the policy functions. It also prints to display how much
        time and how many iterations were necessary to converge to the
        solution.

        PARAMETERS
        ----------
        k : numpy.array
             The grid for the state variable over which the Value Function is
             computed. The resulting policy functions will be computed at the
             gridpoints in this array.
        c0 : numpy.array
             An initial condition for the guess on the policy function for
             consumption.
        tolerance : float (optional, default is 10**(-6))
                    The value against which the sup-norm is compared to when
                    determining whether the algorithm converged or not.

        RETURNS
        -------
        c_opt : numpy.array
                The policy function for consumption, evaluated at the
                gridpoints 'k'.
        k_opt : numpy.array
                The policy function for capital holdings, evaluated at the
                gridpoints 'k'.
        """
        c_old = np.zeros(c0.shape)
        c_old[:] = c0
        n_iter = 0
        criterion = 1
        t0 = time()

        while criterion > tolerance:
            n_iter += 1
            kp = (k ** self.alpha - c_old) + (1 - self.delta) * k
            pc = np.polyfit(k, c_old, 5)
            ctp1 = np.polyval(pc, kp)
            opr = self.alpha * kp ** (self.alpha-1) + 1 - self.delta
            c1 = ctp1 * (self.beta * opr) ** (-1 / self.gamma)
            criterion = np.max(np.abs(c1 - c_old))
            c_old[:] = c1

        t1 = time()

        c_opt = c1
        k_opt = (k ** self.alpha - c_opt) + (1 - self.delta) * k

        print('PFI took {} iterations and {:.3f} seconds to converge'.format(n_iter, t1 - t0))
        return (c_opt, k_opt)


    def solve_proj(self, k, c0, tolerance=1e-6):
        """
        This method takes a grid for the state variable and solves the Bellman
        problem by Policy Function Iteration. As the convergence of the
        projection method depends on the initial condition, an initial
        condition must be provided by the user. The method returns the policy
        functions. It also prints to display how much time and how many
        iterations were necessary to converge to the solution.
        """

        t0 = time()

        c_opt = opt.fsolve(self._euler, c0, args=k)

        t1 = time()
        k_opt = k ** self.alpha - c_opt + (1-self.delta) * k

        print('Direct projection took {:.2f} seconds.'.format(t1-t0))
        return [c_opt, k_opt]


    def plot_solution(self, k, c_opt, k_opt, v=None, figSize=None):
        """
        This method plots the policy functions of this model once they have
        been obtained. It optionally plots the value function if this is
        available. It essentially is a wrapper around matplotlib.pyplot.plot
        with a (optionally custom) grid of plots.

        PARAMETERS
        ----------
        k : numpy.array
             The grid of points over which the policy functions have been
             computed.
        c_opt : numpy.array
                The policy function for consumption.
        k_opt : numpy.array
                The policy function for capital holdings.
        v : numpy.array (optional)
             The value function.
        figSize : tuple
                  A tuple of floats representing the size of the resulting
                  figure in inches, formatted as (width, height).

        RETURNS
        -------
        fig : matplotlib.figure
              The figure object instantiated by this wrapper (mainly for later
              saving to disk).
        ax : list
             The list of matplotlib.axes._subplots.AxesSubplot objects.
        """

        if v is not None:
            fig = plt.subplots(figsize=figSize)

            ax = [None, None, None]
            pltgrid = (2, 4)

            ax[0] = plt.subplot2grid(pltgrid, (0, 0), rowspan=2, colspan=2)
            ax[1] = plt.subplot2grid(pltgrid, (0, 2), colspan=2)
            ax[2] = plt.subplot2grid(pltgrid, (1, 2), colspan=2)

            ax[0].plot(k, v,
                       linewidth=2,
                       color='red',
                       label=r'$V(k)$')
            ax[1].plot(k, k_opt,
                       linewidth=2,
                       color='red',
                       label=r"$k'(k)$",
                       zorder=2)
            ax[2].plot(k, c_opt,
                       linewidth=2,
                       color='red',
                       label=r'$c(k)$')
            ax[1].plot(k, k,
                       linewidth=1,
                       color='black',
                       linestyle='dashed',
                       zorder=1)

            ax[0].set_title('Value function')
            ax[1].set_title('Capital accumulation decision')
            ax[2].set_title('Consumption decision')

        else:
            fig, ax = plt.subplots(nrows=1, ncols=2, figsize=figSize)

            ax[0].plot(k, k_opt,
                       color='red',
                       linewidth=2,
                       zorder=2,
                       label=r"$k'(k)$")
            ax[1].plot(k, c_opt,
                       color='red',
                       linewidth=2,
                       zorder=2,
                       label=r'$c(k)$')
            ax[0].plot(k, k,
                       color='black',
                       linewidth=1,
                       linestyle='dashed',
                       zorder=1)

            ax[0].set_title('Capital accumulation decision')
            ax[1].set_title('Consumption decision')

        for a in range(len(ax)):
            ax[a].axvline(self.k_ss,
                          linewidth=1,
                          color='black',
                          linestyle='dotted',
                          zorder=1)
            ax[a].grid(alpha=0.3)
            ax[a].set_xlabel('$k$')
            ax[a].legend()

        plt.tight_layout()

        return [fig, ax]
