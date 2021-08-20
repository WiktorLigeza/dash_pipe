import dash
import dash_core_components as dcc
import dash_bootstrap_components as dbc
import dash_html_components as html
from dash.dependencies import Output, Input, State
import plotly.graph_objs as go
import plotly.express as px
import pandas as pd
import numpy as np
import dash_table
from data_cleasing import cleaser
from utils.callback_manager import update_main_hist, update_box_plot, \
    update_correlation_heatmap, get_slider_range, save_modified, get_NaNs_pie
from utils.data import DataSet
from utils import html_manager
from utils import df_table_manager

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

data_set = DataSet()
data_set.path = "data\\data.csv"
init_path = "data\\data.csv"
data_set.get_data()
data = data_set.data
html_manager.column_options = data_set.columns
html_manager.activate_dropdown()
bins_list = np.arange(100)
path = ""
range_slider = None
column_description = pd.DataFrame()
sep_text_box_value = ''
path_text_box_value = ''
df_table_manager.data_set = data_set
df_table_manager.activate()

app.layout = html.Div([
    html.Div([
        html.Img(src="/assets/img.webp")], style={'padding-left': '25px', 'padding': '25px'}),

    # LEFT CONTAINER
    html.Div([
        html_manager.text_box_path,
        html_manager.text_box_sep,
        html_manager.save_button,
        html_manager.data_set_radio_buttons,
        html_manager.description_table,
        html_manager.main_histogram,
        html_manager.columns_dropdown,
        html_manager.main_hist_sliders,
    ], className="block-long", style={'float': 'left', 'width': "35%", "margin": "25px"}),
    html.Div(id='hidden-div-1', style={'display': 'none'}),
    html.Div(id='hidden-div-2', style={'display': 'none'}),
    html.Div(id='hidden-div-3', style={'display': 'none'}),
    html.Div(id='hidden-div-4', style={'display': 'none'}),

    # RIGHT CONTAINER
    html.Div([
        df_table_manager.data_frame_table,
    ], className="block", style={'float': 'right', "margin": "25px"}, ),
    html.Div([
        html_manager.box_graph,
    ], className="block", style={'float': 'right', "margin": "25px"}, ),

    # LEFT BOTTOM CONTAINER
    html.Div([
        html_manager.correlation_heatmap,
    ], className="block", style={'float': 'left', "margin": "25px"}, ),

    # RIGHT BOTTOM CONTAINER
    html.Div([
        html_manager.nans_pie,

    ], className="block", style={'float': 'right', "margin": "25px", "width": "40%"}, ),

])


@app.callback(
    Output("columns-dropdown", "options"),
    [Input('read', 'n_clicks')]
)
def read(n):
    global data_set, path_text_box_value
    data_set.path = path_text_box_value
    data_set.get_data()
    html_manager.column_options = data_set.data.columns
    print(data_set.data.columns)
    data_set.column = data_set.data.columns[0]
    return [{'label': opt, 'value': opt} for opt in html_manager.column_options]


@app.callback(
    Output("main-hist-cols", "figure"),
    Output("nans-pie", "figure"),
    Output("range-slider", "min"),
    Output("range-slider", "max"),
    Output("range-slider", "marks"),
    Output("range-slider", "value"),
    Output("range-slider", "step"),
    Output("range-output", "children"),
    [Input('columns-dropdown', 'value'),
     Input('bins-slider', 'value'),
     Input('range-slider', 'value'),
     Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'selected_columns'),
     Input('read', 'n_clicks')
     ])
def update_fig(column, bins, val_range, _, __, table_selected_column, n):
    global data, range_slider, data_set
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == "datatable-interactivity.selected_columns":
        data_set.column = table_selected_column[0]
    if trigger == "columns-dropdown.value":
        data_set.column = column
    if trigger == "range-slider.value" or trigger == "bins-slider.value":
        data_set.range = val_range
        label_output = ["< {} : {} >".format(data_set.range[0], data_set.range[1])]
        print(data_set.column)
        return [update_main_hist(bins, data_set)] + [get_NaNs_pie(data_set)] + \
               list(get_slider_range(data_set, 2)) + label_output
    print("cipeczka 1 ", data_set.column)
    range_list = list(get_slider_range(data_set, 1))
    data_set.range = range_list[0:2]
    label_output = ["< {} : {} >".format(data_set.range[0], data_set.range[1])]
    print("cipeczka 2 ", data_set.column)
    return [update_main_hist(bins, data_set)] + [get_NaNs_pie(data_set)] + \
           range_list + label_output


@app.callback(
    [Output('table', 'columns'), Output('table', 'data')],
    [Input('columns-dropdown', 'value'),
     Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'selected_columns'),
     Input('read', 'n_clicks')
     ]
)
def describe_table(column, rows, derived_virtual_selected_rows, table_selected_column, n):
    global data_set
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == "datatable-interactivity.selected_columns":
        data_set.column = table_selected_column[0]
    else:
        data_set.column = column
    return data_set.description_to_cols_rows_datatable()


@app.callback(
    Output("out-all-types", "children"),
    [Input("path-input", "value")],
)
def cb_render(path_v):
    global path_text_box_value
    path_text_box_value = path_v


@app.callback(
    Output("out-sep", "children"),
    [Input("sep-input", "value")],
)
def sep_render(sep_v):
    global sep_text_box_value
    sep_text_box_value = sep_v


@app.callback(
    Output("hidden-div-2", "children"),
    [Input('set-sep', 'n_clicks')]
)
def set_sep(plus):
    global data_set
    data_set.separator = sep_text_box_value
    raise dash.exceptions.PreventUpdate("cancel the callback")


@app.callback(
    Output("box-graph", "figure"),
    [Input('columns-dropdown', 'value'),
     Input('range-slider', 'value'),
     Input('datatable-interactivity', "derived_virtual_data"),
     Input('datatable-interactivity', "derived_virtual_selected_rows"),
     Input('datatable-interactivity', 'selected_columns'),
     Input('read', 'n_clicks')])
def box_graph(column, range, rows, derived_virtual_selected_rows, table_selected_column, n):
    global data_set
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == "datatable-interactivity.selected_columns":
        if len(table_selected_column) > 0:
            data_set.column = table_selected_column[0]
        else:
            if data_set.data_type == "modified-radio":
                data_set.column = data_set.modified_data.columns[0]
            else:
                data_set.column = data_set.data.columns[0]
    else:
        data_set.column = column
    return update_box_plot(data_set)


@app.callback(
    Output('datatable-interactivity', 'style_data_conditional'),
    Input('datatable-interactivity', 'selected_columns')
)
def update_styles(selected_columns):
    global data_set
    return df_table_manager.update_styles(selected_columns, data_set)


@app.callback(
    Output('datatable-interactivity-container', "children"),
    Input('datatable-interactivity', "derived_virtual_data"),
    Input('datatable-interactivity', "derived_virtual_selected_rows"),
    Input('read', 'n_clicks'))
def update_table(rows, derived_virtual_selected_rows, n):
    global data_set
    trigger = dash.callback_context.triggered[0]["prop_id"]
    if trigger == "datatable-interactivity.derived_virtual_data":
        if data_set.data_type == "original-radio":
            print("You Cant Edit Original Data. Please Edit Modified Data Instead")
            raise dash.exceptions.PreventUpdate("cancel the callback")

    return df_table_manager.update_graphs(rows, derived_virtual_selected_rows, data_set)


@app.callback(
    Output("datatable-interactivity", "data"),
    Output("datatable-interactivity", "columns"),
    Input('radio-buttons-data-type', "value"),
    Input('read', 'n_clicks'))
def update_data(value, n):
    global data_set
    if value == "original-radio":
        data_set.display_data = data_set.modified_data.copy(deep=True)
        columns = [{'name': col, 'id': col, "selectable": True} for col in
                   data_set.data.columns]
        val = data_set.data.to_dict('records')
    else:
        data_set.modified_data = data_set.display_data.copy(deep=True)
        columns = [{'name': col, 'id': col, "deletable": True, "selectable": True} for col in
                   data_set.modified_data.columns]
        val = data_set.modified_data.to_dict('records')

    return val, columns


@app.callback(
    Output("correlation-heatmap", "figure"),
    [Input('columns-dropdown', 'value'),
     Input('read', 'n_clicks')])
def update_fig(value, n):
    global data_set
    return update_correlation_heatmap(data_set)


@app.callback(
    Output('hidden-div-4', "children"),
    [Input('save-modified-button', "n_clicks")],
)
def save(n):
    global data_set
    if n == 0:
        print("init")
    else:
        print("save: {}".format(n))
        data_set.path = init_path
        save_modified(data_set, n)
    raise dash.exceptions.PreventUpdate("cancel the callback")


if __name__ == "__main__":
    app.run_server(debug=True)
