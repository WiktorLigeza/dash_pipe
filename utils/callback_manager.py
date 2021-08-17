import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


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
    temp_ = pd.DataFrame()
    temp_["q"] = data_set.data[data_set.column]
    temp_["w"] = data_set.data[data_set.column]
    temp_["e"] = data_set.data[data_set.column]
    print(temp_)

    return px.box(temp_)


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
    

