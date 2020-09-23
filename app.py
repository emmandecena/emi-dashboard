import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server

# data

df = pd.read_csv('/data/Grid_demand_trends_20200923223432.csv', parse_dates=True)
df = df.drop(columns="Trading period")

df['year'] = pd.DatetimeIndex(df['Period start']).year
df['month'] = pd.DatetimeIndex(df['Period start']).month


# figure
fig = px.line(df, x='Period start', y="Demand (GWh)", color='Region ID')

app.layout = html.Div(children=[
    html.H1(children='Grid Demand Forecasting'),
    html.Div(children='''
        Dash: A web application framework for Python.
    '''),

    dcc.Graph(
        id='example-graph',
        figure=fig
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
