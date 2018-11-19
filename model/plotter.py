import itertools
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from model.parameterframe import ParameterFrame


class Plotter(object):

    def __init__(self, trace_df):

        self.trace_df = trace_df

    def __repr__(self):
        p, k = self.get_dimensions()
        return '(p = ' + str(p) + ', k= ' + str(k) + ')'

    def get_trace_df(self):
        return self.trace_df

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
