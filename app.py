import dash
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
import plotly.express as px
import pandas as pd
import plotly.offline as py
import pathlib

from fbprophet import Prophet
from fbprophet.plot import plot_plotly, plot_components_plotly, plot_forecast_component_plotly, plot_seasonality_plotly
from dash.dependencies import Input, Output

app = dash.Dash(
    __name__,
    meta_tags = [{"name": "viewport",
        "content": "width=device-width, initial-scale=1"}],
)

server=app.server

# data

df=pd.read_csv('data/Grid_demand_trends_20200923223432.csv',
               parse_dates = True)
df=df.drop(columns = ["Trading period", "Region ID", "Period end"])
# renaming the columns, demand in GWh
df.columns=['date', 'region', 'demand']
# Date is day,month,year format since NZ
df['date']=pd.to_datetime(df['date'], dayfirst = True)
df['region']=df['region'].astype('category')

region_list = df["region"].unique()
# functions

def description_card():
    """

    :return: A Div containing dashboard title & descriptions.
    """
    return html.Div(
        id="description-card",
        children=[
            html.H5("Emmanuel Decena"),
            html.H3("Regional Electricity Demand Forecast for New Zealand"),
            html.Div(
                id="intro",
                children="Monthly demand data taken from the Electricity Market Information of the Electricity Authority. The Python package Prophet is used to calculate the forecasts",
            ),
        ],
    )
# controls
def generate_control_card():
    """

    :return: A Div containing controls for graphs.
    """
    return html.Div(
        id="control-card",
        children=[
            html.P("Select Region"),
            dcc.Dropdown(
                id="clinic-select",
                options=[{"label": i, "value": i} for i in region_list],
                value=region_list[0],clearable=False,searchable=False
            ),
            html.Br(),
            html.Div(
                id="desc",
                children="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.",
            ),
 ],
)

# plot

# layout

app.layout=html.Div(
    id = "app-container",
    children = [
        # Banner
        html.Div(
            id="banner",
            className="banner",
            children=[html.Img(src=app.get_asset_url("plotly_logo.png"))],
        ),
        # Left column
        html.Div(
            id="left-column",
            className="four columns",
            children=[description_card(),generate_control_card()],
        ),
        # Right column
        html.Div(
            id="right-column",
            className="eight columns",
            children=[
                # Patient Volume Heatmap
                html.Div(
                    id="patient_volume_card",
                    children=[
                        html.B("Actual and Predicted Electricity Demand from January 2012 - July 2021"),
                        html.Hr(),
                        dcc.Graph(id="demand-graph"),
                    ],
                ),
                # Patient Wait time by Department
                html.Div(
                    id="wait_time_card",
                    children=[
                        html.B("Forecasting Method"),
                        html.Hr(),
                        html.Div(id="wait_time_table",
                                 children="Lorem ipsum dolor sit amet, consectetur adipisicing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum."),
                    ],
                ),
            ],
        ),
    ],
)



# callbacks

@ app.callback(
    Output('demand-graph', 'figure'),
    [Input('clinic-select', 'value')],
)

def update_demand(value):
    filtered_df=df[df.region == value]
    df_prophet=filtered_df.drop(columns = "region")

    df_prophet.columns=['ds', 'y']
    m=Prophet()
    m.fit(df_prophet)

    future= m.make_future_dataframe(periods = 12, freq = 'M')
    forecast=m.predict(future)
# figure

    figure= plot_plotly(m, forecast, xlabel = 'Date', ylabel = 'Demand (GWH)')

    return figure



if __name__ == '__main__':
    app.run_server(debug = True)
