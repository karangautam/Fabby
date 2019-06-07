import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

import plotly.graph_objs as go
import squarify
import pandas as pd
app = dash.Dash()
server = app.server
app.config.supress_callback_exceptions = True
rfm = pd.read_csv('rfm.csv')
rfm['Counts'] = rfm.groupby(['Segment'])['CustomerID'].transform('count')
app.layout = html.Div([
    dcc.Graph(id='treemap')
])

@app.callback(
    Output('treemap', 'figure'),
    [Input('treemap', 'value')])
def treemap(value):
    
 
    
    #values = [500, 433, 78, 25, 25, 7]
    values = rfm['Segment'].value_counts().values
    index = rfm['Segment'].value_counts().index
    parents_segment = rfm['Segment'].head(20).values
    childs = rfm['CustomerID'].head(20).values
    segment_counts= rfm['Counts'].head(20).values


    # Choose colors from http://colorbrewer2.org/ under "Export"

    trace = go.Sunburst(
        ids=childs,
        labels=parents_segment,
        values=segment_counts,
        outsidetextfont = {"size": 20, "color": "#377eb8"},
        marker = {"line": {"width": 2}},maxdepth=2)

    layout = go.Layout(
        margin = go.layout.Margin(t=0, l=0, r=0, b=0))

  #  fig = {'data':  trace, 'layout':layout}
    fig = go.Figure([trace], layout)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)