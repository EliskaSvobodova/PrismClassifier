import logging
from typing import Tuple

import pandas as pd
import numpy as np


def get_prep_data(filename: str, y_name: str) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    df = pd.read_csv(filename)
    df = prep_binning(df)
    X_train, X_test, y_train, y_test = train_test_split(df.drop(y_name, axis=1), df[y_name])
    return X_train, X_test, y_train, y_test


def prep_binning(df_orig: pd.DataFrame, max_values: int = 5):
    df = df_orig.copy()

    def _numerical(col_name):
        return df.dtypes[col_name] == np.int64 or df.dtypes[col_name] == np.float64

    logging.info("Preprocessing - binning:")
    for col in df.columns:
        if _numerical(col) and df[col].nunique() > max_values:
            logging.info(f"{col} - too many values ({df[col].nunique()})")
            df[col] = pd.cut(df[col], bins=max_values, labels=range(1, max_values + 1))
        else:
            logging.info(f"{col} - ok ({df[col].nunique()} = {', '.join(str(v) for v in df[col].unique())})")
    return df


def train_test_split(X: pd.DataFrame, y: pd.Series, test_size=0.2) -> Tuple[pd.DataFrame, pd.DataFrame, pd.Series, pd.Series]:
    df = pd.concat([X, y], axis=1)
    train = df.sample(frac=(1 - test_size))
    test = df.drop(train.index)
    return train.iloc[:, :-1], test.iloc[:, :-1], train.iloc[:, -1], test.iloc[:, -1]
