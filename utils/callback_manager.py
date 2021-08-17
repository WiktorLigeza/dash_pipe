import plotly.graph_objects as go
import plotly.express as px
import pandas as pd
from data_cleasing import cleaser


def update_main_hist(bins, data_set):
    try:
        if data_set.data_type == "modified-radio":
            trace_close = go.Histogram(x=data_set.modified_data[data_set.column], nbinsx=int(bins))
            print(len(data_set.modified_data[data_set.column]))
        else:
            trace_close = go.Histogram(x=data_set.data[data_set.column], nbinsx=int(bins))
    except:
        trace_close = go.Histogram(x=data_set.data[data_set.column], nbinsx=int(bins))
    d = [trace_close]
    if isinstance(data_set.column, list):
        data_set.column = data_set.column[0]
    layout = go.Layout(
        title=data_set.column,
        margin=dict(l=40, r=25, b=30, t=40),
        autosize=True)

    return {
        "data": d,
        "layout": layout
    }


def update_box_plot(data_set):

    df = pd.DataFrame()
    df = data_set.data[data_set.column]
    original_list = df.values.tolist()
    iqr_list = cleaser.IQR_outliners(df)
    zscore_list = cleaser.zscore_outliners(df)

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
    corr = data_set.data.corr()

    trace = go.Heatmap(z=corr.values,
                       x=corr.index.values,
                       y=corr.columns.values)
    d = [trace]

    if isinstance(data_set.column, list):
        data_set.column = data_set.column[0]

    return {
        "data": d
    }


def set_range_slider(data_set):
    print("dooopa:", data_set.range)
    

