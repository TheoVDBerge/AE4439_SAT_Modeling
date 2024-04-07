# from dash import Dash, html

# app = Dash(__name__)

# app.layout = html.Div([
#     html.Div(children='Hello World')
# ])

# if __name__ == '__main__':
#     app.run(debug=True)

# Import packages
from dash import Dash, html, dash_table
import pandas as pd

# Incorporate data
df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminder2007.csv')

# Initialize the app
app = Dash(__name__)

# App layout
app.layout = html.Div([
    html.Div(children='My First App with Data'),
    dash_table.DataTable(data=df.to_dict('records'), page_size=(len(df)/2))
])

# Run the app
if __name__ == '__main__':
    app.run(debug=True)
    
# https://dash-example-index.herokuapp.com/country-distances