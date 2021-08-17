import dash_html_components as html
import dash_table
import dash_core_components as dcc
import dash_bootstrap_components as dbc
from dash.dependencies import Output, Input, State

column_options = ""
activate = False

### IMAGES
logo = html.Div([
    html.Img(src="/assets/img.webp")], style={'padding-left': '25px', 'padding': '25px'}),

### DATA TABLES
description_table = html.Div([
    html.Div([
        dash_table.DataTable(
            id='table',
            data=[],
            style_table={'overflowX': 'auto'},
            style_header={'color': 'rgb(237, 27, 37)',
                          'backgroundColor': 'rgb(125, 125, 125)',
                          'fontWeight': 'bold'
                          },
        )], style={"margin": "5%", 'width': '90%'})
])

### TEXT BOXES
text_box_path = html.Div([
                             dcc.Input(id="path-input", type="text", placeholder="path"),
                             dbc.Button('read', id='read', color="light", className="b-1")
                         ] + [html.Div(id="out-all-types")], style={"margin-left": "5%"})

text_box_sep = html.Div([
                            dcc.Input(id="sep-input", type="text", placeholder="separator default: ,"),
                            dbc.Button('set', id='set-sep', color="light", className="b-1")
                        ] + [html.Div(id="out-sep")], style={"margin-left": "5%", "float": "left"})

### FIGURES
main_histogram = html.Div([
    dcc.Graph(id='main-hist-cols')], style={'width': '90%', "margin": "5%"})

box_graph = html.Div([
    dcc.Graph(id='box-graph')]
    , style={'width': '90%', 'margin': '5%', "display": "inline-block"})

### DROP DOWNS
columns_dropdown = None

### SLIDERS
main_hist_sliders = html.Div([
    html.Div([
        dcc.Slider(
            id='bins-slider',
            min=0,
            max=100,
            marks={i: '{}'.format(i) for i in [0, 25, 50, 75, 100]},
            value=10),

        dcc.RangeSlider(
            id='range-slider',
            min=0,
            max=20,
            step=0.5,
            value=[5, 15]
        ),
    ], style={'width': '100%', 'font-color': '#bd0b23', 'margin-top': '1%', 'display': "inline-block"})
], style={'width': '50%', "margin-right": "5%", 'font-style': 'normal',
          'display': "inline-block", 'float': 'right'})


### RADIO BUTTONS
data_set_radio_buttons = html.Div([dcc.RadioItems(
    id='radio-buttons-data-type',
    options=[
        {'label': 'Original Data', 'value': 'original-radio'},
        {'label': 'Modified Data', 'value': 'modified-radio'}
    ],
    value='modified-radio'
)], style={"float": "right", "margin-right": "5%", "display": "inline-block"})


image_what_we_do = html.Div([

], className="what-we-do")


message_box = html.Div([
        dcc.ConfirmDialog(
            id='confirm',
            message='Danger danger! Are you sure you want to continue?',
        ),

        dcc.Dropdown(
            options=[
                {'label': i, 'value': i}
                for i in ['Safe', 'Danger!!']
            ],
            id='dropdown'
        ),
        html.Div(id='output-confirm')
    ])


correlation_heatmap = html.Div([
    dcc.Graph(id='correlation-heatmap')], style={'width': '90%', "margin": "5%"})


def activate_dropdown():
    global columns_dropdown
    columns_dropdown = html.Div([
        dcc.Dropdown(
            id='columns-dropdown',
            # multi= True,
            options=[{'label': opt, 'value': opt} for opt in column_options],
            value=column_options[0]
        )], style={'width': '25%', "margin-left": "5%", 'font-style': 'normal',
                   'float': 'left', 'display': "inline-block"})
