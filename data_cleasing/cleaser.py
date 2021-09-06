import numpy as np
import pandas as pd
from sklearn.ensemble import IsolationForest
from sklearn.manifold import TSNE
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA


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


def check_nans(dataframe):
    df_nan = dataframe.copy()
    cols = df_nan.columns.values.tolist()
    ctr = 0

    for x in cols:
        col = df_nan[x].to_numpy()

        if np.isnan(col).any():
            nans_sum = sum(np.isnan(col))
            df_len = col.shape[0]
            nan_ratio = nans_sum / df_len

            if 0.00000001 < nan_ratio < 0.25:
                df_nan[x] = df_nan[x].fillna(-1)
                ctr += 1

            if nan_ratio >= 0.25:
                del df_nan[x]
                ctr += 1

    return df_nan

def check_str(dataframe):
    df_str = dataframe.copy()
    cols = df_str.columns.values
    for x in cols:
        if np.any([isinstance(val, str) for val in df_str[x]]):
            del df_str[x]
    return df_str


def drop_cols_from_list(col_list, dataframe):
    df_copy = dataframe.copy()
    for x in col_list:
        del df_copy[x]
    df_nonans = check_str(df_copy)
    df_nonans = check_nans(df_nonans)

    return df_nonans

def pca_preproc(df, features, target):
    features = df.columns.to_list()
    y = df.loc[:,[target]].values
    x = df.loc[:, features].values
    x = StandardScaler().fit_transform(x)
    np.stack(x)
    pca = PCA(n_components=3)
    principalComponents = pca.fit_transform(x)
    principalDf = pd.DataFrame(data = principalComponents
                 , columns = ['principal component 1', 'principal component 2', 'principal component 3'])
    df = pd.concat([principalDf, df[target]], axis = 1)
    return df

X_embedded = None
counter = 0

def t_sne(df):
    global X_embedded, counter

    if counter == 0:
        X_embedded = TSNE(n_components=3).fit_transform(df)
        counter = -1

    X_embedded_df = pd.DataFrame(data = X_embedded
             , columns = ['principal component 1', 'principal component 2', 'principal component 3'])
    return X_embedded_df


def clean_df(col_list, dataframe, target):
    df = drop_cols_from_list(col_list, dataframe)
    features = df.columns.to_list()
    df = pca_preproc(df, features, target)
    tsne_df = t_sne(df)
    return tsne_df, df


# to rebuild (merge with pca_preproc above)
def reconstruction_score(original_data, reconstructed_data, normalized=True):
    loss = np.sum((np.array(original_data)-np.array(reconstructed_data))**2, axis=1)
    if normalized==True:
        loss = (loss-np.min(loss))/(np.max(loss)-np.min(loss))
    loss = pd.Series(data=loss,index=original_data.index)
    return loss


def pca_preproc_rec(df, features, target):
    df_copy = df.copy()
    std = StandardScaler()
    pca = PCA(n_components=3)

    df_reduced = pd.DataFrame(pca.fit_transform(std.fit_transform(df_copy)), index=df_copy.index)
    df_inverse_pca = pd.DataFrame(pca.inverse_transform(df_reduced), columns=df.columns, index=df.index)
    df_inversed = pd.DataFrame(std.inverse_transform(df_inverse_pca), columns=df_inverse_pca.columns,
                               index=df_inverse_pca.index)

    return df_reduced, pca, df_inversed, df_copy


def clean_df_rec(col_list, dataframe, target):
    df = drop_cols_from_list(col_list, dataframe)
    features = df.columns.to_list()
    df_reduced, pca, df_inverse_pca, df_copy = pca_preproc_rec(df, features, target)
    return df_reduced, pca, df_inverse_pca, df_copy

