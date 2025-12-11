import pandas as pd
import numpy as np
from dash import Dash, html, dash_table, dcc, callback, Output, Input
import dash_bootstrap_components as dbc
import plotly.express as px
import plotly.graph_objects as go

from simulatore import *
from grafici import *


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
                    dcc.Graph(figure=barProduzione),
                            ])
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
                    dcc.Dropdown(id='dropdownProd', options=
                                 ['Mais', 'Riso', 'Grano'], value='Mais'),
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
                    dbc.CardHeader('Quantità totale prodotta'),
                    dcc.Graph(figure=pieProduzione), 
                        ])
                ]),
    ])
    ])



TAB_CLIMA = dbc.Container([
    dbc.Row([
                dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Precipitazioni medie mensili"),
                    dbc.CardBody(dcc.Graph(id="precipitazioni", figure=barPrecipitazioni))
                    ]),
            ]),
                dbc.Col([
                dbc.Card([
                    dbc.CardHeader("Temperatura media mensile"),
                    dbc.CardBody(dcc.Graph(figure=lineTemperatura))
                    ])
            ])                      
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                    dbc.CardHeader("Umidità"),
                    dbc.CardBody(dcc.Graph(figure=areaUmidita))
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
                value = risorse_amb['emissioni'].mean(),
                domain = {'x': [0, 1], 'y': [0, 1]},
                title = {'text': "Emissioni"},
                gauge={
                'threshold': {
                'line': {'color': "red", 'width': 4},
                'thickness': 1,
                'value': 8000},
                'bar': {'color':'black'},
                'steps': [
                    {'range': [0, 5000], 'color': "green"},
                    {'range': [5000, 6500], 'color': "yellow"},
                    {'range': [6500, 8000], 'color': "red"},
        ],
                })
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
                dcc.Graph(figure=lineRicavomais)
            ])
        ], width=4),
            dbc.Col([
            dbc.Card([
                dbc.CardHeader("Ricavo riso"),
                dcc.Graph(figure=lineRicavoriso)
            ])
        ], width=4),
            dbc.Col([
            dbc.Card([
                dbc.CardHeader("Ricavo grano"),
                dcc.Graph(figure=lineRicavograno)
            ])
        ]),
    ]),
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Spese'),
                dbc.CardBody([
                    dcc.Graph(id='barSpese'),
                    ]),
                dbc.CardFooter([
                    dbc.Checklist(id='checkSpese', 
                              options=[
                              {'label':'Manodopera','value':'manodopera'},
                              {'label':'Pesticidi','value':'pesticidi'},
                              {'label':'Fertilizzanti','value':'fertilizzanti'}
                              ], 
                              value=['manodopera'],
                              inline=True,
                              style={'padding': 10, 'text-align':'center'})
                   ])
            ])
        ]),
        dbc.Col([
            dbc.Card([
                dbc.CardHeader('Spesa totale'),
                dbc.CardBody([
                dcc.Graph(figure=pieCosto)               
                ])
            ])
        ])
    ]),
    dbc.Row([
        dbc.Col([
                dbc.Card([
                    dbc.CardHeader('Guadagno mensile'),
                    dbc.CardBody([
                        dcc.Graph(id='waterfallVendite'),
                        dcc.Slider(
                            id='slider',
                            min=2,
                            max=12,
                            value=2,
                            step=1,
                            marks={k: v for k, v in date_formattate.items()}),
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
                                "border": "1px solid #d1a85a"}])
                ])
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
            dbc.Tab(label="Economia", tab_id="economia")]
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

    if selezione == 'Mais':
        coltura='mais'
        valore='valoreMais'
    elif selezione == 'Riso':
        coltura='riso'
        valore='valoreRiso'
    elif selezione == 'Grano':
        coltura='grano'
        valore='valoreGrano'
        coltura='grano'

    colonne=[
        {'name':'Data', 'id':'index'},
        {'name':'Tonnellate', 'id': coltura},
        {'name':'Valore', 'id': valore}]


    return colonne


@app.callback(
    Output("lineColture", "figure"),
    Input("checklist_colture", "value"),
)
def aggiorna(selezione):
    fig = px.line(colture, y=selezione, x=DATA)

    fig.update_traces(
    hovertemplate="%{y:.1f}t<br>%{x}",
    name="Tonnelate"
    )

    fig.update_layout(
    yaxis_title="Tonnellate",
    xaxis_title="Mese"
    )

    return fig


@app.callback(
   Output("barSpese", "figure"), 
   Input("checkSpese", "value"),
)
def aggiorna(selezione):
    fig = px.line(spese, y=selezione, x=DATA, markers=True)

    fig.update_traces(
    hovertemplate="%{y:.1f} €<br>%{x}",
    name="Euro (€)"
    )

    fig.update_layout(
    yaxis_title="Spese (€)",
    xaxis_title="Mese"
    )


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

    fig = px.line(risorse_amb, y=y, x=DATA)

    fig.update_traces(
    hovertemplate="%{y:.1f} Kg<br>%{x}",
    name="Tonnelate"
    )

    fig.update_layout(
    yaxis_title="Emissioni (Kg)",
    xaxis_title="Mese"
    )

    return fig 


@app.callback(
        Output('waterfallVendite','figure'),
        Input('slider', 'value')
        )
def calcolodelta(mese):
    mese = date_formattate[mese]
    waterfallDf = ricavoColture.reset_index()


    waterfallDf['index'] = waterfallDf['index'].dt.strftime('%d-%m-%Y')
    mesi = list(waterfallDf['index'])    

    idx=mesi.index(mese)

    df_prev = (waterfallDf[waterfallDf['index'] == mesi[idx-1]]).set_index('index')
    df_curr = (waterfallDf[waterfallDf['index'] == mesi[idx]]).set_index('index')
    riga_corr = df_curr.loc[mesi[idx]]
    riga_prev = df_prev.loc[mesi[idx-1]]

    delta = riga_corr - riga_prev
    delta = delta.to_frame(name="value")


    waterfall = go.Figure(go.Waterfall(
    orientation='v',
    x=delta.index,
    y=delta['value'],
    ))

        

    return waterfall




if __name__ == "__main__":
    app.run()

