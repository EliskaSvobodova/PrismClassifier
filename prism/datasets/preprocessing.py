import logging
from typing import Tuple

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split


def get_prep_data(filename: str, y_name: str) -> Tuple[pd.DataFrame, pd.DataFrame]:
    df = pd.read_csv(filename)
    train, test = train_test_split(df)
    train, bins = prep_binning(train, y_name, retbins=True)
    test = prep_binning(test, y_name, bins=bins)
    return train, test


def prep_binning(df_orig: pd.DataFrame, y_name: str, max_values: int = 5, bins=None, retbins=False):
    df = df_orig.copy()

    def _numerical(col_name):
        return df.dtypes[col_name] == np.int64 or df.dtypes[col_name] == np.float64

    new_bins = {}
    logging.info("Preprocessing - binning:")
    for col in df.drop(y_name, axis=1).columns:
        if _numerical(col) and df[col].nunique() > max_values:
            logging.info(f"{col} - too many values ({df[col].nunique()})")
            if bins is None:
                df[col], b = pd.qcut(df[col], q=max_values, precision=2, retbins=True, duplicates='drop')
                df[col] = df[col].cat.codes
                new_bins[col] = b
            elif col in bins:
                df[col] = pd.cut(df[col], bins=bins[col])
                df[col] = df[col].cat.codes
                new_bins[col] = bins[col]
        else:
            logging.info(f"{col} - ok ({df[col].nunique()} = {', '.join(str(v) for v in df[col].unique())})")
    if retbins:
        return df, new_bins
    else:
        return df
