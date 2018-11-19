import itertools
import numpy as np
import pandas as pd


class ParameterFrame(object):

    """Object to convert simulated parameters to pd.DataFrame

    parameter_list : list of matrices
        list of either Beta or Sigma matrices

    name : (str)
        name parameters i.e. 'beta' or 'sigma'

    """

    def __init__(self, parameter_list, name):

        self.param_list = parameter_list
        self.name = name

        try:
            self.k = self.param_list[0].shape[1]  # number of questions
        except IndexError:
            self.k = self.param_list[0].shape[0]  # Dealing with vector Sigma

        self.p = self.param_list[0].shape[0]  # number of factors

    def _get_loop_tuples(self):

        return list(itertools.product(range(self.p), range(self.k), ))

    def get_list_of_estimations(self, d1, d2):

        try:
            return [param[d1, d2] for param in self.param_list]
        except IndexError:
            if d1 == d2:
                return [param[d1] for param in self.param_list]
            else:
                return [0 for param in self.param_list]

    def _calc_param_trace_dict(self):

        self.param_trace_dict = dict()
        for tup in self._get_loop_tuples():
            k, p = tup[0], tup[1]
            self.param_trace_dict['{0}_{1};{2}'.format(
                self.name, k, p)] = self.get_list_of_estimations(k, p)

    def get_trace_df(self):

        try:
            return self.trace_df
        except AttributeError:
            self._calc_trace_df()
            return self.trace_df

    def _calc_trace_df(self):

        try:
            self.trace_df = pd.DataFrame(
                self.param_trace_dict, index=list(range(len(self.param_list))))
        except AttributeError:
            self._calc_param_trace_dict()
            self.trace_df = pd.DataFrame(
                self.param_trace_dict, index=list(range(len(self.param_list))))
