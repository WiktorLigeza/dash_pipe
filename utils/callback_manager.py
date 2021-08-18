import plotly.graph_objs as go
import plotly.express as px
import pandas as pd


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


def get_slider_range(data_set, type_=1):
    max_ = data_set.modified_data[data_set.column].max()
    min_ = data_set.modified_data[data_set.column].min()
    marks_ = {i: '{}'.format(i) for i in [min_, round(((max_+min_)/2), 2), max_]}
    step_ = (max_-min_)/100

    if type_ == 1:
        value_ = [min_, max_]
    else:
        value_ = data_set.range

    return min_, max_, marks_, value_, step_


def get_x(data_set, datum):
    check_x(data_set)
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
        print("dddoopsko", data_set.range)

