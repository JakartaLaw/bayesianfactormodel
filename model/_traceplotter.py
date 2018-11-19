import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model.parameterframe import ParameterFrame
from model.plotter import Plotter


# GEMTE SIKKERT KOPI HVIS JEG SKULLE FUCKE NOGET OP! KAN SLETTES MED ER GOD FOR REFERENCE
class TracePlotter(Plotter):

    """

    parameter_list : list of matrices
        list of either Beta or Sigma matrices

    name : (str)
        name parameters i.e. 'beta' or 'sigma'
    """

    def __init__(self, trace_df):
        super()__init__(trace_df=trace_df)

    def __repr__(self):
        p, k = self.get_dimensions()
        return '(p = ' + str(p) + ', k= ' + str(k) + ')'

    def get_trace_df(self):
        return self.trace_df

    def plot_nxn_traces(self, n, skip_obs=None):

        df = self.get_trace_df()
        fig, axes = plt.subplots(n, n, figsize=(n * 4, n * 4))

        for i, col in enumerate(df.columns):

            if i < n**2:

                obs, index = df[col][skip_obs:], df.index[skip_obs:]
                dim1 = int(i % n)
                dim2 = int(((n - 1) - np.floor(((n**2) - i - 1) / n)))
                axes[dim1, dim2].plot(index, obs, label=col)
                axes[dim1, dim2].legend()

    def plot_4x4_traces(self, skip_obs=None):
        """plots first 16 traces"""

        return self.plot_nxn_traces(4, skip_obs=skip_obs)

    def plot_3x3_traces(self, skip_obs=None):
        """plots first 9 traces"""

        return self.plot_nxn_traces(3, skip_obs=skip_obs)

        return fig

    def plot_diagonal_traces(self, skip_obs=None):
        """plots diagonal traces"""

        p, k = self.get_dimensions()
        assert p == k, 'Not diagonal matrix'

        fig, axes = plt.subplots(p, 1, figsize=(8, 3 * p))
        df = self.get_trace_df()

        for col in df.columns:

            # takes the last element which will be '<SOME STRING>_x;y'
            k = col.split('_')[-1]
            v = k.split(';')
            if int(v[0]) == int(v[1]):
                axes[int(v[0])].plot(df.index[skip_obs:], df[col][skip_obs:], label=col)
                axes[int(v[0])].legend()

        return fig

    def get_dimensions(self):
        """returns (p, k)"""

        df = self.get_trace_df()

        d0, d1 = 0, 0
        for col in df.columns:

            _d0, _d1 = self._decompose_column_index(col)

            if _d0 > d0:
                d0 = _d0

            if _d1 > d1:
                d1 = _d1

        return d0 + 1, d1 + 1

    def _decompose_column_index(self, col):
        # takes the last element which will be '<SOME STRING>_x;y'
        k = col.split('_')[-1]
        v = k.split(';')

        _d0, _d1 = int(v[0]), int(v[1])
        return _d0, _d1
