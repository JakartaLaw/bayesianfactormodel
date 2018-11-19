import numpy as np
import pandas as pd

from collections import defaultdict
from model.parameterframe import ParameterFrame
from model.plotter import Plotter

from collections import defaultdict


class Parameters(Plotter):

    def __init__(self, trace_df):

        super().__init__(trace_df)

    @property
    def k():
        p, k = self.get_dimensions()
        return k

    @property
    def p():
        p, k = self.get_dimensions()
        return p

    def _calc_param_mean_dict(self, skip_obs=None):

        try:
            self._calc_helper_param_mean_dict(skip_obs=skip_obs)

        except AttributeError:
            self._calc_param_trace_dict()
            self._calc_helper_param_mean_dict(skip_obs=skip_obs)

    def _calc_helper_param_mean_dict(self, skip_obs):
        self.param_mean_dict = dict()
        for param_name in self.trace_df.columns:

            param_obs = self.trace_df[param_name][skip_obs:]
            self.param_mean_dict[param_name] = np.mean(param_obs)

    def params_to_df(self):

        params_unordered = self._convert_to_dimension_dict()
        params_ordered = self._order_to_df(params_unordered)

        return pd.DataFrame(params_ordered)

    def _convert_to_dimension_dict(self):
        #self.k, self.p

        param_to_df_unordered = defaultdict(list)
        for param_name, param_val in self.param_mean_dict.items():

            (d1, d2) = self._decompose_column_index(param_name)
            param_to_df_unordered[d2].append((d1, param_val))

        return param_to_df_unordered

    def _order_to_df(self, param_to_df_unordered):

        params_to_df = dict()
        for key, tup_list in param_to_df_unordered.items():
            params_to_df[key] = self._return_ordered_by_index_params(tup_list)

        return params_to_df

    @staticmethod
    def _return_ordered_by_index_params(tup_list):

        def sorter(tup): return tup[0]
        tup_list.sort(key=sorter)
        return [tup[1] for tup in tup_list]
