import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
from dash.dependencies import Input, Output

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# data

df = pd.read_csv('data/Grid_demand_trends_20200923223432.csv', parse_dates=True)
df = df.drop(columns=["Trading period","Region ID","Period end"])
#renaming the columns, demand in GWh
df.columns = ['date', 'region','demand']
#Date is day,month,year format since NZ
df['date']= pd.to_datetime(df['date'], dayfirst=True)
df['region'] = df['region'].astype('category')

# layout
app.layout = html.Div(children=[
    html.H1(children='Grid Demand Forecasting [on-going]'),
    html.Div(children='''
        by Emmanuel Decena.
    '''),

    dcc.RadioItems(
        id='region-selector',
        options=[
            {'label': 'Upper North Island', 'value': 'Upper North Island'},
            {'label': 'Central North Island', 'value': 'Central North Island'},
            {'label': 'Lower North Island', 'value': 'Lower North Island'},
            {'label': 'Upper South Island', 'value': 'Upper South Island'},
            {'label': 'Lower South Island', 'value': 'Lower South Island'},
        ], value='Upper North Island'
    ),

    html.Div([
        dcc.Graph(
            id='demand-graph'
        )
    ])

])

# callbacks
@app.callback(
    Output('demand-graph', 'figure'),
    [Input('region-selector', 'value')])

def update_figure(value):
    filtered_df = df[df.region == value ]

# figure
    figure = px.line(filtered_df, x='date', y="demand", color='region')
    figure.update_layout(transition_duration=500)

    return figure



if __name__ == '__main__':
    app.run_server(debug=True)
