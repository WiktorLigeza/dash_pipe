import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest


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
    # plt.bar(range(missing_value_df.index.shape[0]), missing_value_df)
    pct_missing_value_df = missing_value_df[missing_value_df['percent_missing']>0]
    return pct_missing_value_df