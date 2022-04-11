import logging

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


class DataPreprocessor:
    def __init__(self, filename: str, y_name: str):
        self.y_name = y_name
        df = pd.read_csv(filename)
        self.train, self.test = train_test_split(df)
        self.binning_info = None

    def get_train_test(self):
        return self.train, self.test

    def apply_binning(self, max_values: int = 5):
        self.binning_info = {}

        def _numerical(df, col_name):
            return df.dtypes[col_name] == np.int64 or df.dtypes[col_name] == np.float64

        logging.info("Preprocessing - binning:")
        for col in self.train.drop(self.y_name, axis=1).columns:
            if _numerical(self.train, col) and self.train[col].nunique() > max_values:
                logging.info(f"{col} - too many values ({self.train[col].nunique()})")
                self.train[col], bins = pd.qcut(self.train[col], q=max_values, precision=2, retbins=True, duplicates='drop')
                self.binning_info[col] = {i: str(c) for i, c in enumerate(self.train[col].cat.categories)}
                self.train[col] = self.train[col].cat.codes
                self.test[col] = pd.cut(self.test[col], bins=bins)
                self.test[col] = self.test[col].cat.codes
            else:
                logging.info(f"{col} - ok ({self.train[col].nunique()} = {', '.join(str(v) for v in self.train[col].unique())})")
