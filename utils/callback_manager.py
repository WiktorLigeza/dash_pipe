import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
from data_cleasing import cleaser

inter = 0


def update_main_hist(bins, data_set):
    try:
        if data_set.data_type == "modified-radio":
            trace_close = go.Histogram(x=get_x(data_set, data_set.modified_data[data_set.column]), nbinsx=int(bins))
            print(len(data_set.modified_data[data_set.column]))
        else:
            trace_close = go.Histogram(x=get_x(data_set, data_set.data[data_set.column]), nbinsx=int(bins))
    except Exception as e:
        print(e)
        trace_close = go.Histogram(x=get_x(data_set, data_set.data[data_set.column]), nbinsx=int(bins))
    d = [trace_close]
    if isinstance(data_set.column, list):
        if len(data_set.column) > 0:
            data_set.column = data_set.column[0]
        else:
            data_set.column = data_set.modified_data.columns[0]
    layout = go.Layout(
        title=data_set.column,
        margin=dict(l=40, r=25, b=30, t=40),
        autosize=True)

    return {
        "data": d,
        "layout": layout
    }


def update_box_plot(data_set):
    global inter
    inter += 1
    print(data_set.range, inter)
    df = get_x(data_set, data_set.data[data_set.column])
    original_list = df.values.tolist()
    iqr_list = cleaser.IQR_outliers(df)
    zscore_list = cleaser.zscore_outliers(df)
    dc = {'Original': original_list, 'IQR': iqr_list, 'Z-Score': zscore_list}
    df_new = pd.DataFrame.from_dict(dc, orient='index')
    df_new = df_new.transpose()
    fig = go.Figure()
    fig.update_layout(
        title="Filtering from outliners",
        yaxis_title="column value",
    )
    for col in df_new:
        fig.add_trace(go.Box(y=df_new[col].values, name=df_new[col].name))
    return fig


def update_correlation_heatmap(data_set):
    df = get_x(data_set, data_set.modified_data[data_set.column])
    corr = data_set.data.corr()

    trace = go.Heatmap(z=corr.values,
                       x=corr.index.values,
                       y=corr.columns.values)
    d = [trace]

    if isinstance(data_set.column, list):
        if len(data_set.column) > 0:
            data_set.column = data_set.column[0]
        else:
            data_set.column = data_set.data.columns[0]

    return {
        "data": d
    }


def get_slider_range(data_set, type_=1):
    if str(type(data_set.modified_data[data_set.column].max())) == "<class 'pandas.core.series.Series'>":
        if data_set.data_type == "modified-radio":
            data_set.column = data_set.modified_data.columns[0]
        else:
            data_set.column = data_set.data.columns[0]
    max_ = float(round(data_set.modified_data[data_set.column].max(), 2))
    min_ = float(round(data_set.modified_data[data_set.column].min(), 2))
    marks_ = {i: '{}'.format(i) for i in [min_, round(((max_ + min_) / 2), 2), max_]}
    step_ = float((max_ - min_) / 100)

    if type_ == 1:
        value_ = [min_, max_]
    else:
        value_ = data_set.range

    return min_, max_, marks_, value_, step_


def get_x(data_set, datum):
    try:
        temp = datum[datum >= data_set.range[0]]
        return temp[temp <= data_set.range[1]]
    except:
        return datum


def check_x(data_set):
    max_ = data_set.modified_data[data_set.column].max()
    min_ = data_set.modified_data[data_set.column].min()
    if data_set.range is None:
        data_set.range = [min_, max_]


def save_modified(data_set, n):
    print(data_set.path)
    new_path = data_set.path.replace('.csv', '_modified_{}.csv'.format(n))
    data_set.modified_data.to_csv(new_path)


def get_NaNs_pie(data_set):
    datum = get_x(data_set, data_set.modified_data[data_set.column])
    nans = data_set.modified_data[data_set.column].isnull().sum()
    df_len = len(datum)
    list_to_df = []
    list_to_df.append(nans)
    list_to_df.append(abs(df_len - nans))
    labels = ['NaNs', 'Rest']
    fig = go.Figure(data=[go.Pie(labels=labels, values=list_to_df, hole=.3, title="Nans")])
    fig.update_layout(
        title_text="The ratio of NaNs: {} at range <{} : {}>".format(data_set.column,
                                                                     data_set.range[0], data_set.range[1]))

    return fig
