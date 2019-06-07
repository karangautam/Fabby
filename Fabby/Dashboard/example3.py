import pandas as pd
from datetime import timedelta
import numpy as np
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

sales = pd.read_excel('Online Retail.xlsx')

sales.dropna(subset=['CustomerID'], inplace=True)
sales['amount'] = sales['Quantity'] * sales['UnitPrice']
sales = sales[~(sales.Quantity<0)]
sales = sales[sales.UnitPrice>0]
sales.CustomerID = sales.CustomerID.astype('Int64')
cs_df=sales
PercentSales =  np.round((cs_df.groupby(["CustomerID"]).amount.sum().\
                          sort_values(ascending = False).head(51).sum()/cs_df.groupby(["CustomerID"]).\
                          amount.sum().sort_values(ascending = False).sum()) * 100, 2)
g = cs_df.groupby(["CustomerID"]).amount.sum().sort_values(ascending = False).head(51)

PercentSales1 =  np.round((cs_df.groupby(["CustomerID"]).amount.sum().\
                          sort_values(ascending = False).head(10).sum()/cs_df.groupby(["CustomerID"]).\
                          amount.sum().sort_values(ascending = False).sum()) * 100, 2)
g1 = cs_df.groupby(["CustomerID"]).amount.sum().sort_values(ascending = False).head(10)

PercentSales2 =  np.round((cs_df.groupby(["CustomerID"]).amount.count().\
                          sort_values(ascending = False).head(10).sum()/cs_df.groupby(["CustomerID"]).\
                          amount.count().sort_values(ascending = False).sum()) * 100, 2)
g2 = cs_df.groupby(["CustomerID"]).amount.count().sort_values(ascending = False).head(10)


app.layout = html.Div([
    dcc.Graph(id='bargraph1')
])

@app.callback(
    Output('bargraph1', 'figure'),
    [Input('bargraph1', 'value')])
def update_bargraph1(value):
	x_value = g.index.astype('str')
	y_value = g.values
	trace = [go.Bar(x=x_value, y=y_value)]
	return {"data": trace,
            "layout": go.Layout(xaxis=dict(type='category'),
                height=700, title="Top Customers: {:3.2f}% Sales Amount".format(PercentSales),
                )
            }

if __name__ == '__main__':
    app.run_server(debug=True)