import dash_table
import pandas as pd
import dash_html_components as html
from utils.data import DataSet
import dash_core_components as dcc

data_frame_table = None
data_set = DataSet()


def activate():
    global data_frame_table, data_set
    data_frame_table = html.Div([
        dash_table.DataTable(
            id='datatable-interactivity',
            columns=[
                {"name": i, "id": i, "deletable": True, "selectable": True} for i in data_set.data.columns
            ],
            data=data_set.data.to_dict('records'),
            editable=True,
            filter_action="native",
            sort_action="native",
            sort_mode="multi",
            column_selectable="single",
            row_selectable="multi",
            row_deletable=True,
            selected_columns=[],
            selected_rows=[],
            page_action="native",
            page_current=0,
            page_size=10,
            style_cell={'minWidth': '70px'},
            style_table={"padding": "200", 'overflowX': 'auto'},
        ),
        html.Div(id='datatable-interactivity-container')
    ], style={"margin": "5%", 'width': '90%'})


def update_styles(selected_column, ds):
    ds.column = selected_column
    return [{
        'if': {'column_id': i},
        'background_color': '#D2F3FF'
    } for i in ds.column]


def update_graphs(rows, derived_virtual_selected_rows, ds):
    if derived_virtual_selected_rows is None:
        derived_virtual_selected_rows = []

    ds.modified_data = ds.modified_data if rows is None else pd.DataFrame(rows)

    colors = ['#7FDBFF' if i in derived_virtual_selected_rows else '#0074D9'
              for i in range(len(ds.modified_data))]
    return [
        dcc.Graph(
            id=column,
            figure={
                "data": [
                    {
                        "x": ds.modified_data["itemDiameter"],
                        "type": "histogram",
                        "marker": {"color": colors},
                    }
                ],
                "layout": {
                    "xaxis": {"automargin": True},
                    "yaxis": {
                        "automargin": True,
                        "title": {"text": column}
                    },
                    "height": 250,
                    "margin": {"t": 10, "l": 10, "r": 10},
                },
            },
        )
        for column in ["pop", "lifeExp", "gdpPercap"] if column in ds.modified_data
    ]
