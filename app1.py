# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 15:44:41 2020

@author: Andrea
"""

import dash
import dash_core_components as dcc
import dash_html_components as html
import plotly.graph_objs as go
from dash.dependencies import Input,Output,State
import pandas as pd
import pandas_datareader.data as web
from datetime import datetime

app = dash.Dash()

server = app.server

nsdq = pd.read_excel('main_bovespa.xlsx')
nsdq.set_index('Symbol', inplace = True)
#nsdq = nsdq.set_index('Symbol')

options = []

for tic in nsdq.index:
    mydict = {}
    mydict['label'] = str(nsdq.loc[tic]['Name']) + ' ' + tic # Apple Co. AAPL
    mydict['value'] = tic
    options.append(mydict)

app.layout = html.Div([
                html.H1('Bovespa Dashboard (Dados do Yahoo Finance)'),
                html.Div([
                        html.H3('Selecionar ação:', style={'paddingRight':'30px'}),
                        dcc.Dropdown(id='my_stock_picker',
                             options = options,
                             value=['PETR4.SA'],
                             multi=True
                         )
              ], style={'display':'inline-block','verticalAlign':'top', 'width':'30%'}),
                html.Div([html.H3('Selecionar período:'),
                          dcc.DatePickerRange(id='my_date_picker',
                                              min_date_allowed=datetime(1993,1,1),
                                              max_date_allowed=datetime.today(),
                                              start_date = datetime(2018,1,1),
                                              end_date = datetime.today())
                  ], style={'display':'inline-block'}),
                    html.Div([
                            html.Button(id='submit_button',
                                        n_clicks=0,
                                        children='Atualizar',
                                        style={'fontSize':24,'marginLeft':'30px'})
                    ], style={'display':'inline-block'}),
              dcc.Graph(id='my_graph',
                        figure={'data':[
                                {'x':[1,2],'y':[3,1]}
                    ], 'layout':{'title':'Default Title'}}
        )
])

@app.callback(Output('my_graph', 'figure'),
              [Input('submit_button','n_clicks')],
              [State('my_stock_picker','value'),
               State('my_date_picker', 'start_date'),
               State('my_date_picker', 'end_date')])

def update_graph(n_clicks, stock_ticker, start_date, end_date):
    start = datetime.strptime(start_date[:10],'%Y-%m-%d')
    end = datetime.strptime(end_date[:10],'%Y-%m-%d')
    
    traces = []
    for tic in stock_ticker:
        df = web.DataReader(tic, 'yahoo', start, end)
        traces.append({'x':df.index,'y':df['Close'], 'name':tic})
        
    fig = {'data':traces,
           'layout':{'title':stock_ticker}}
    return fig

if __name__ == '__main__':
    app.run_server()