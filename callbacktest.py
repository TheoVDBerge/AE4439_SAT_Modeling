import dash
import pandas as pd

from dash import dash_table as dt
from dash import dcc
from dash import html
from dash.dependencies import Input
from dash.dependencies import Output
# from main_data import df
#%%
df = pd.read_csv("https://raw.githubusercontent.com/plotly/datasets/master/solar.csv")
#%%
app = dash.Dash(__name__)
app.title = 'SAT modeling project'

# states = df.State.unique().tolist()

app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id="filter_dropdown",
            options=list(df['State'].unique()),
            placeholder="-Select a State-",
            multi=True,
            style={'width': '50%', 'maxWidth': 'none'}
            # value=df.State.values,
        ),
        dt.DataTable(
            id="table-container",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records")
        ),
        
    # html.Style("""
    #     .dropdown .Select-menu-outer {
    #         width: 40% !important;  /* Set dropdown menu width to match dropdown box */
    #     }
    # """)
    ])


@app.callback(
    Output("table-container", "data"), 
    Input("filter_dropdown", "value")
)
def display_table(state):
    if state is None or len(state) == 0:
        return df.to_dict("records")
    else:
        filtered_df = df[df.State.isin(state)]
        return filtered_df.to_dict("records")


if __name__ == "__main__":
    app.run_server(debug=True)