import pandas as pd
import numpy as np
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from simulatore import *


app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP,'./assets/custom.css']
)


TAB_PRODUZIONE = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Andamento temporale"),
                dbc.CardBody(
                    dbc.Row([
                        dbc.Col([
                           dcc.Graph(id="lineColture"),
                            ]),
                       dbc.Col([
                    dcc.Graph(figure=px.bar(colture, y=['mais', 'riso', 'grano'], x=DATA))         
                            ]),
                        ])),
                dbc.Checklist(id="checklist_colture", 
                              options=[
                              {'label':'Mais','value':'mais'},
                              {'label':'Riso','value':'riso'},
                              {'label':'Grano','value':'grano'}
                              ], 
                              value=['mais'],
                              inline=True,
                              style={'padding': 20, 'text-align':'center'})
            ])
        ]),
           
        ]),
    dbc.Row([
        dbc.Col([
             dbc.Card([
                 dbc.CardHeader('Scegliere la coltura desiderata'),
                 dbc.CardBody([
                    dcc.Dropdown(id='dropdownProd', options=['mais', 'grano', 'riso'], value='mais'),
                    dash_table.DataTable(
                        id='tableColture',
                        data=filtro.to_dict('records'), 
                        columns=[],
                        sort_action='native')
                     ])
                 ]),
        ]),
        dbc.Col([ 
                dbc.Card([
                    dcc.Graph(figure=px.pie(sommaColture, names='Coltura', values='Valore')), 
                        ])
                ]),
    ])
    ])
    
TAB_CLIMA = dbc.Container([
    dbc.Row([
                dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Precipitazioni"),
                    dbc.CardBody(dcc.Graph(id="precipitazioni", figure=px.bar(clima, y=['precipitazioni'], x=DATA)))
                    ]),
            ]),
                dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Temperatura"),
                    dbc.CardBody(dcc.Graph(id="temperatura",figure=px.line(clima, y=['temperatura'], x=DATA, range_y=(20, 40), markers=True)))
                    ])
            ]),
                dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Umidità"),
                    dbc.CardBody(dcc.Graph(id="umidità", figure=px.histogram(x=x,y=y)))
                    ])
            ])
                    
    ]),

    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Emissioni ambientali di Co2'),
                dbc.CardBody([
                    dbc.Row([
                    dbc.Col([
                    dcc.Graph(id='lineEmiss')], 
                            width=7),
                dbc.Col([
            dcc.Graph(
                figure=go.Figure(go.Indicator(
                mode = "gauge+number",
                value =risorse_amb['emissioni'].mean(),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Emissioni"},
                gauge={
                'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 0.75,
                'value': 8000}})
                            ))
                    ])
                ])                
            ]),
                dbc.Checklist(id="checklistEmiss", 
                              options=[
                              {'label':'Visualizza Limite Emissioni','value':'limite'}],
                              value=['limite'],
                              switch=True,
                              style={"padding": 20})
            ])
        ]),
    ])
])



TAB_ECONOMIA = dbc.Container([
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader("Ricavo mais"),
                dcc.Graph(figure=px.line(df, x=DATA, y=['valoreMais']))
            ])
        ], width=4),
            dbc.Col([
            dbc.Card([
                dbc.CardHeader("Ricavo riso"),
                dcc.Graph(id='prova', figure=px.line(df, x=DATA, y=['valoreRiso']))
            ])
        ], width=4),
            dbc.Col([
            dbc.Card([
                dbc.CardHeader("Ricavo grano"),
                dcc.Graph(id='prova', figure=px.line(df, x=DATA, y=['valoreGrano']))
            ])
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('temp'),
                dbc.CardBody([
                    dcc.Graph(id='barSpese'),
                    ]),
                dbc.CardFooter([
                    dbc.Checklist(id='checkSpese', options=['manodopera','pesticidi','fertilizzanti'], value=['manodopera'])
                    ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Spesa totale'),
                dbc.CardBody([
                dcc.Graph(id='piePrezzi', figure=px.pie(sommaSpese, names='Spesa', values='Valore'))               
                ])
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([ 
                 dbc.Card([
                  dash_table.DataTable(
                          data=df_dict,
                          columns=[
                            {"name": "Data", "id": 'index' },
                            {"name": "Costo Pesticidi", "id": "pesticidi"},
                            {"name": "Costo fertilizzanti", "id": "fertilizzanti"},
                            {"name": "Costo Manodopera", "id": "manodopera"},
                            {"name": "Ricavo Riso", "id":"valoreRiso"},
                            {"name": "Ricavo Grano", "id": "valoreGrano"},
                            {"name": "Ricavo Mais", "id": "valoreMais"},
                            {"name": "Ricavo Tot", "id":'totale'}
                        ],
                    style_data_conditional=[{
                        "if": {"row_index": "odd"},
                        "backgroundColor": "#f8f8f8"},
                        {
                            'if':{
                                "filter_query": "{{totale}} = {}".format(df['totale'].max()),
                                'colunm_id': 'Totale'},
                                "fontWeight": "bold", 
                                "border": "1px solid #d1a85a"}]

                        )])
        ])
    ])
])

app.layout = dbc.Container([
    dbc.Tabs(
        id="tabs",
        active_tab="produzione",
        children=[
            dbc.Tab(label="Produzione", tab_id="produzione"),
            dbc.Tab(label="Clima e Risorse Ambientali", tab_id="clima"),
            dbc.Tab(label="Economa", tab_id="economia"),
        ]
    ),
    html.Div(id="tab_content",
        style={
        "width": "100%",
        "height": "700px",
        "overflow": "auto",
        "border": "1px solid #ccc",
        "padding": "10px"
    })
])

@app.callback(
    Output("tab_content", "children"), 
    Input("tabs", "active_tab"),
)
def cambia(at):
    if   at == 'produzione':
        return TAB_PRODUZIONE
    elif at == 'clima':
        return TAB_CLIMA
    elif at == 'economia':
        return TAB_ECONOMIA


@app.callback(
    Output('tableColture', 'columns'),
    Input('dropdownProd', 'value')
)
def aggiorna(selezione):

    coltura= None
    valore = None

    if selezione == 'mais':
        coltura='mais'
        valore='valoreMais'
    elif selezione == 'riso':
        coltura='riso'
        valore='valoreRiso'
    elif selezione == 'grano':
        coltura='grano'
        valore='valoreGrano'


    colonne=[
        {'name':'Data', 'id':'index'},
        {'name':'Tonnellate', 'id': coltura},
        {'name':'Valore', 'id': valore}]


    return colonne
 
print(sommaColture)

@app.callback(
    Output("lineColture", "figure"),
    Input("checklist_colture", "value"),
)
def aggiorna(selezione):
    fig = px.line(colture, y=selezione, x=DATA)
    return fig


@app.callback(
   Output("barSpese", "figure"), 
   Input("checkSpese", "value"),
)
def aggiorna(selezione):
    fig = px.line(spese, y=selezione, x=DATA, markers=True)
    return fig


@app.callback(
   Output("lineEmiss", "figure"), 
   Input("checklistEmiss", "value"),
)
def aggiorna(selezione):
    y=['emissioni']
    if selezione == ['limite']:
        soglia = np.full(12,8000)
        y.append(soglia)

    fig = px.line(risorse_amb, y=y, x=DATA, markers=True)
    return fig 

if __name__ == "__main__":
    app.run()

