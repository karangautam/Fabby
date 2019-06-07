import os
import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#from app import app

app = dash.Dash()
server = app.server


app.config.supress_callback_exceptions = True
rfm = pd.read_csv('rfm.csv')

app.layout = html.Div([
    dcc.Graph(id="my-graph")
])


@app.callback(
    Output("my-graph", "figure"),
    [Input('my-graph', 'value')])

def ugdate_figure(value):
    z = rfm['Frequency']
    trace = [go.Scatter3d(
        x=rfm['Recency'], y=rfm['Frequency'], z=rfm['Monetary'],
        mode='markers', marker={'size': 8 })]
    return {"data": trace,
            "layout": go.Layout(
                height=700, title="Recency Frequency Monetary",
                paper_bgcolor="#f3f3f3",
                scene={"aspectmode": "cube", "xaxis": {"title": "Recency" },
                       "yaxis": {"title": "Frequency" },
                       "zaxis": {"title": "Monetary" }})
            }
            
        

if __name__ == '__main__':
    app.run_server(debug=True)

