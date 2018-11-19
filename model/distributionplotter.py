import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model.parameterframe import ParameterFrame
from model.plotter import Plotter


class DistributionPlotter(Plotter):

    """Plots distributions

    parameter_list : list of matrices
        list of either Beta or Sigma matrices

    name : (str)
        name parameters i.e. 'beta' or 'sigma'

    tail_mass : (float)
        float in [0, 100] to denote percentage of mass to exclude from distribution plot
    """

    def __init__(self, trace_df, tail_mass):

        super().__init__(trace_df)
        self.tail_mass = tail_mass

    def _calc_bins(self, obs, n_bins):

        min_val, max_val = np.percentile(
            obs, self.tail_mass), np.percentile(obs, 100 - self.tail_mass)
        return list(np.linspace(min_val, max_val, n_bins))

    def plot_diagonal_hists(self, skip_obs=None, n_bins=40):
        """plots diagonal traces"""

        p, k = self.get_dimensions()
        assert p == k, 'Not diagonal matrix'

        fig, axes = plt.subplots(p, 1, figsize=(8, 3 * p))
        df = self.get_trace_df()

        for col in df.columns:

            v0, v1 = self._decompose_column_index(col)

            if v0 == v1:
                obs = df[col][skip_obs:]
                bins = self._calc_bins(obs, n_bins)
                axes[v0].hist(obs, bins=bins, label=col)
                axes[v1].legend()

        return fig

    def plot_nxn_hists(self, n, skip_obs=None, n_bins=40):

        df = self.get_trace_df()
        fig, axes = plt.subplots(n, n, figsize=(n * 4, n * 4))

        for i, col in enumerate(df.columns):

            if i < n**2:

                obs, index = df[col][skip_obs:], df.index[skip_obs:]
                bins = self._calc_bins(obs, n_bins)
                dim1 = int(i % n)
                dim2 = int(((n - 1) - np.floor(((n**2) - i - 1) / n)))
                axes[dim1, dim2].hist(obs, label=col, bins=bins)
                axes[dim1, dim2].legend()

        return fig

    def plot_4x4_hists(self, skip_obs=None, n_bins=40):
        """plots first 16 traces"""

        return self.plot_nxn_hists(n=4, skip_obs=skip_obs, n_bins=n_bins)

    def plot_3x3_hists(self, skip_obs=None, n_bins=40):
        """plots first 9 traces"""

        return self.plot_nxn_hists(n=3, skip_obs=skip_obs, n_bins=n_bins)
