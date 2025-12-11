from simulatore import *
import plotly.express as px
import plotly.graph_objects as go

#linecolture

barProduzione = px.bar(colture, y=['mais', 'riso', 'grano'], x=DATA)

barProduzione.update_traces(
    hovertemplate="%{y:.1f}t<br>%{x}",
    name="Tonnelate"
    )

barProduzione.update_layout(
    yaxis_title="Tonnellate",
    xaxis_title="Mese"
    )




pieProduzione = px.pie(sommaColture, names='Coltura', values='Valore')

pieProduzione.update_traces(
    hovertemplate="%{y:.1f}t<br>%{x}",
    name="Tonnelate"
    )

pieProduzione.update_layout(
    yaxis_title="Tonnellate",
    xaxis_title="Mese"
    )




barPrecipitazioni = px.bar(clima, y=['precipitazioni'], x=DATA)

barPrecipitazioni.update_traces(
    hovertemplate="%{y:.1f}t<br>%{x}",
    name="Tonnelate"
    )

barPrecipitazioni.update_layout(
    yaxis_title="Tonnellate",
    xaxis_title="Mese"
    )




lineTemperatura = px.line(clima, y=['temperatura'], x=DATA, markers=True)

lineTemperatura.update_layout(
    yaxis_title="Temperatura (°C)",
    xaxis_title="Mese",
    hovermode="x"
)

lineTemperatura.update_traces(
    hovertemplate="%{y:.1f} °C<br>Mese: %{x}"
)


areaUmidita = go.Figure()

areaUmidita.add_trace(
    go.Scatter(
        x=DATA,
        y=clima['umidita'],
        fill='tozeroy',
        name="Stagione umida"
    ))

areaUmidita.add_trace(
    go.Scatter(
        x=DATA,
        y=clima['umidita_secca'],
        fill='tozeroy',
        name="Stagione secca"
    )
)

areaUmidita.update_layout(
    yaxis_title="Umidità (%)",
    xaxis_title="Mese",
)


#lineEmissioni
#gaugeEmissioni


lineRicavomais =px.line(df, x=DATA, y=['valoreMais'])

lineRicavomais.update_layout(
    yaxis_title="Guadagno (€)",
    xaxis_title="Mese",
    hovermode="x"
)

lineRicavomais.update_traces(
    hovertemplate="%{y:.1f}€<br>Mese: %{x}"
)


lineRicavoriso = px.line(df, x=DATA, y=['valoreRiso'])

lineRicavoriso.update_layout(
    yaxis_title="Guadagno (€)",
    xaxis_title="Mese",
    hovermode="x"
)

lineRicavoriso.update_traces(
    hovertemplate="%{y:.1f}€<br>Mese: %{x}"
)


lineRicavograno = px.line(df, x=DATA, y=['valoreGrano']) 

lineRicavograno.update_layout(
    yaxis_title="Guadagno (€)",
    xaxis_title="Mese",
    hovermode="x"
)

lineRicavograno.update_traces(
    hovertemplate="%{y:.1f}€<br>Mese: %{x}"
)


'''
lineCosto
'''


pieCosto = px.pie(sommaSpese, names='Spesa', values='Valore') 


