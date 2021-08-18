import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


def IQR_outliers(df):
    Q = df.quantile([0.25, 0.75])
    iqr = Q.values[1] - Q.values[0]
    lower_inner_fence = Q.values[0] - (iqr * 1.5)
    lower_outer_fence = Q.values[0] - (iqr * 3)
    upper_inner_fence = Q.values[1] + (iqr * 1.5)
    upper_outer_fence = Q.values[1] + (iqr * 3)
    df = df[(lower_outer_fence <= df) & (df <= upper_outer_fence)]
    return df.values.tolist()


def zscore_outliers(df):
    mean = df.mean()
    std = df.std()
    filtered_list = []
    for x in df:
        zscore = (x - mean) / std
        if -3 <= zscore <= 3:
            filtered_list.append(x)
    return filtered_list


def outliers_detection(df):
    _df = df.copy()
    _df.dropna(inplace=True)
    clf = IsolationForest(random_state=2020, contamination=0.01, max_features=10)
    outliers = clf.fit_predict(_df)
    outliers = pd.DataFrame(outliers, columns=['is_outlier'], index=_df.index)
    outliers.index = _df.index
    outliers['is_outlier'] = outliers['is_outlier'].map(lambda x: True if x == -1 else False)
    return outliers


def pct_of_missing_values(df):
    percent_missing = df.isnull().sum() * 100 / len(df)
    missing_value_df = pd.DataFrame({'percent_missing': percent_missing})
    missing_value_df.sort_values('percent_missing', inplace=True, ascending=False)
    pd.set_option('display.max_rows', 10)
    pct_missing_value_df = missing_value_df[missing_value_df['percent_missing'] > 0]
    return pct_missing_value_df
